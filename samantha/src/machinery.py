import torch
import torch.nn.functional as F
from enum import Enum
import requests
from typing import Any, List, Dict, Sequence, Type
from datetime import datetime, timedelta
import transitions
from integration.whatsapp.whatsapp_client import WhatsAppClient

from samantha.src.configs import (
    SessionLocal,
    ChatHistory,
    VAStage,
    scheduler,
    redis_conn,
    get_device,
    fine_tuned_model,
    fine_tuned_tokenizer,
    cefr_grammar_model,
    cefr_grammar_tokenizer,
    id2label,
    odoo_message
)


TOLERANCE = 3 # seconds of wait ...
INACTIVITY = 60 # seconds of wait for user inactivity.
SOURCE_USER = "human"
SOURCE_LLM = "ai"
DEFAULT_STATE = "draft"

device = get_device()



class SchedulerMachine(transitions.Machine):
    def __init__(self,  msisdn: str, campaign: str, wtsapp_client: WhatsAppClient) -> None:
        states = ["draft", "new", "recording", "evaluation", "appointment", "draft_appointment"]
        #TODO: meter deterctor de prompt-injection al principio
        #TODO: IMPORTANTE: debe estar en memoria para rapido acceso. ciclico, viejos se van borrando.
        self.data = DataManager()

        self.msisdn = msisdn
        self.campaign = campaign
        self.wtsapp_client = wtsapp_client

        self.chat_len = len(self.chat_history)

        m_state = self.data.get_state(msisdn, campaign)
        transitions.Machine.__init__(self, states=states, initial=m_state['state'])
        self.add_ordered_transitions()


    def draft_module(self, text: str, chat_history: list[str], utterance_type: str) -> str:
        data = {'text': text, 'chat_history': chat_history, 'utterance_type': utterance_type}
        response = requests.post("http://localhost:9091/llm/draft", json=data)
        response = response.json()
        return response['llm']
    
    
    def new_module(self, text: str, chat_history: list[str], utterance_type: str) -> str:
        data = {'text': text, 'chat_history': chat_history, 'utterance_type': utterance_type}
        response = requests.post("http://localhost:9091/llm/new", json=data)
        response = response.json()
        return response['llm']
    
    
    def recording_module(self, text: str, chat_history: list[str], utterance_type: str) -> str:
        data = {'text': text, 'chat_history': chat_history, 'utterance_type': utterance_type}
        response = requests.post("http://localhost:9091/llm/recording", json=data)
        response = response.json()
        return response['llm']
    
    
    def evaluation_module(self,text: str, chat_history: list[str], utterance_type: str) -> str:
        data = {'text': text, 'chat_history': chat_history, 'utterance_type': utterance_type}
        response = requests.post("http://localhost:9091/llm/evaluation", json=data)
        response = response.json()
        return response['llm']


    def infer_utterance_type(self, text: str) -> str:
        fine_tuned_model.eval()
        fine_tuned_model.to(device)
        inputs = fine_tuned_tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            return_tensors='pt',
            truncation=True
        )
        # Extract input tensors
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)

        # Perform inference
        with torch.no_grad():
            outputs = fine_tuned_model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()
        
        return id2label[predicted_class]
    
    
    def grammar_probas_scores(self, text: str):
        inputs = cefr_grammar_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        # Extract input IDs and attention mask from tokenization output
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        # Perform inference
        with torch.no_grad():
            logits = cefr_grammar_model(input_ids=input_ids, attention_mask=attention_mask).logits

        # Apply softmax to get probabilities
        probabilities = F.softmax(logits, dim=1)
        # Convert probabilities to a list
        probabilities_list = probabilities.squeeze().tolist()
        probabilities_list = {cefr_grammar_model.config.id2label[i]: p for i, p in enumerate(probabilities_list)}
        p_max = max(probabilities_list, key=lambda x: probabilities_list[x])
        return probabilities_list, p_max

    
    def entry(self, text: str, utterance_type: str) -> str:
        #TODO: model for find utterence type
        # Tokenize the input text
        import time
        start_time = time.time()
        end_time = (time.time() - start_time)
        self.state = self.data.get_state(self.msisdn, self.campaign)['state']
        response = self.router(text, utterance_type)
        return response
        # self.hist(text, response)
        # return utterance_type, end_time

    def router(self, text: str, utterance_type: str) -> str: 
        if self.state == "draft" and text == "#1": # form completed
            try:
                odoo_message.dummy_applicant(self.msisdn) # work because its the #1 thread ? ...
            except Exception as ex:
                print(f"Problemas con odoo rpc en threas {ex}")
            self.step_completed()
            return "Thank you for complete the basic form 🙌🏼 The next step is about filling the assessment below ⤵️"
        
        if self.state == "new" and text.startswith("#2"): #assessment completed
            text = text.replace("#2 ", '')
            self.step_completed()
            self.validate_grammar(text)
            return "Hey, thank you very much! You've taken a significant step forward—congratulations! 🚀 The final step is to send me a voice note 🗣️ lasting no more than 2 minutes for evaluation purposes."
        
        if self.state == "draft_appointment":
            pass

        #TODO: return appointment signal just in case.
        if self.state == "draft":
            response = self.draft_module(text, self.chat_history, utterance_type)
            if len(self.chat_history) == 0:
                welcome = """Hello and welcome! 🎉 We're excited to assist you with your recruitment journey. Whether you have questions about your application, need help scheduling an interview we're here to help. Let's get started """
                response = list(response)
                response[0] = welcome + response[0]
        elif self.state == "new":
            response = self.new_module(text, self.chat_history, utterance_type)
        elif self.state == "recording":
            response = self.recording_module(text, self.chat_history, utterance_type)
        elif self.state == "evaluation": #TODO: TypeError: SchedulerMachine.evaluation_module() takes 2 positional arguments but 4 were given
            response = self.evaluation_module(text, self.chat_history, utterance_type)

        if utterance_type == "continue_later":
            pick = "Could you please choose a date 📆 from the list below ⤵️ for us to continue our conversation? Thanks a lot!"
            return f"{response[0]}\n{pick}"
        
        if utterance_type == "stop_continue":
            pick = "If you want, I can contact you at another time. Just let me know a date that works best for you from the options below. 📅"
            return f"{response[0]}\n{pick}"
        
        return response[0]
    

    def manage_audio(self, audio_id: str):
        if self.state == "recording":
            self.step_completed()
            _, audio = self.wtsapp_client.process_audio(audio_id, self.msisdn, self.campaign)
            message = "Your voice note has been received! ✅ thanks a lot! You've made great progress—well done! 🚀 We have successfully completed the process."
            self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=message)
            #TODO: call method API here to evaluate audio.
            print(audio)
            return
        if self.state == "evaluation":
            message = "Your audio has been received and is currently being validated! 🎧"
            self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=message)
            return
        
        message = "Please switch to text communication for the time being. Appreciate it! 💬"
        self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=message)

    
    @property
    def now_(self):
        return datetime.now().astimezone()

    def eta_(self, s=10):
        return datetime.now().astimezone() + timedelta(seconds=s)

    def __call__(self, message: str, whatsapp_id: str) -> None:
        return self.message_deliver(message, whatsapp_id)

    def message_firer(self, source: str, whatsapp_id: str):
        now = self.now_
        unreaded_messages = self.data.get_unreaded_messages(self.msisdn, self.campaign)
        if len(unreaded_messages) == 1:
            self.data.update_collected(unreaded_messages)

        unreaded_messages_collected = " ".join([u['message'] for u in unreaded_messages])
        if len(unreaded_messages) > 1:
            readed, collected = True, True
            scheduler.add_job(self.data.add_chat_history_db, 'date', run_date=None, args=[self.msisdn, self.campaign, unreaded_messages_collected, SOURCE_USER, whatsapp_id, now, readed, collected])
            self.data.add_chat_history(self.msisdn, self.campaign, unreaded_messages_collected, SOURCE_USER, whatsapp_id, now, readed=True, collected=True)

        utterance_type = self.infer_utterance_type(text=unreaded_messages_collected)
        llm_response = self.entry(text=unreaded_messages_collected, utterance_type=utterance_type)
        print(f"🤖 {llm_response}")
        #TODO: send BACK to WhatsApp here !!
        self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=llm_response)
        readed, collected = True, True
        scheduler.add_job(self.data.add_chat_history_db, 'date', run_date=None, args=[self.msisdn, self.campaign, llm_response, SOURCE_LLM, whatsapp_id, now, readed, collected])
        self.data.add_chat_history(self.msisdn, self.campaign, llm_response, SOURCE_LLM, whatsapp_id, now, readed=True, collected=True)

        if utterance_type == "stop_continue":
            previous_inactivity_id = redis_conn.get(f"inactivity_report_job:{self.msisdn}:{self.campaign}")
            if previous_inactivity_id:
                # Remove the previous inactivity job
                if isinstance(previous_inactivity_id, bytes):
                    previous_inactivity_id = previous_inactivity_id.decode('utf-8')
                    try: 
                        scheduler.remove_job(previous_inactivity_id)
                    except Exception as ex:
                        print(f'{previous_inactivity_id} {ex}')
        

    def inactivity_firer(self, source: str, whatsapp_id: str):
         #TODO: send BACK to WhatsApp here !!
        self.state = self.data.get_state(self.msisdn, self.campaign)['state']
        if self.state == "draft":
            message = f"🤖 Don't forget to take a moment to complete the form! It's easy and only takes 1-2 minutes 😊📝"
            self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=message)
        elif self.state == "new":
            message = f"🤖 Just a friendly reminder to complete the evaluation 🌟—you're one step closer to your hiring! 🚀😊"
            self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=message)
        elif self.state == "recording":
            message = f"🤖 Please don't forget the voice note 🗣️! It's the last step, and it shouldn't be more than 2 minutes. Thank you! 😊"
            self.wtsapp_client.send_text_message(phone_number=self.msisdn, message=message)


    def message_deliver(self, message: str, whatsapp_id: str):
        sending_date = self.now_
        scheduler.add_job(self.data.add_chat_history_db, 'date', run_date=None, args=[self.msisdn, self.campaign, message, SOURCE_USER, whatsapp_id, sending_date])
        self.data.add_chat_history(self.msisdn, self.campaign, message, SOURCE_USER, whatsapp_id, sending_date)

        latest_message = self.data.get_latest_message(self.msisdn, self.campaign)
        if latest_message:
            sending_date = latest_message['sending_date']
            now = self.now_
            difference_in_seconds = (now - sending_date).total_seconds()

            # Check if a previous message_firer jobs is scheduled
            previous_job_id = redis_conn.get(f"message_firer_job_id:{self.msisdn}:{self.campaign}")
            if previous_job_id:
                # Remove the previous job
                if isinstance(previous_job_id, bytes):
                    previous_job_id = previous_job_id.decode('utf-8')
                    try: 
                        scheduler.remove_job(previous_job_id)
                    except Exception as ex:
                        print(f'{previous_job_id} {ex}')

            previous_inactivity_id = redis_conn.get(f"inactivity_report_job:{self.msisdn}:{self.campaign}")
            if previous_inactivity_id:
                # Remove the previous job
                if isinstance(previous_inactivity_id, bytes):
                    previous_inactivity_id = previous_inactivity_id.decode('utf-8')
                    try: 
                        scheduler.remove_job(previous_inactivity_id)
                    except Exception as ex:
                        print(f'{previous_inactivity_id} {ex}')

        eta = self.eta_(s=TOLERANCE)
        inactivity = self.eta_(s=INACTIVITY)
        new_job = scheduler.add_job(self.message_firer, 'date', run_date=eta, args=[SOURCE_USER, whatsapp_id])
        inactivity_report_job = scheduler.add_job(self.inactivity_firer, 'date', run_date=inactivity, args=[SOURCE_USER, whatsapp_id])

        # Store the new job ID in Redis
        redis_conn.set(f"message_firer_job_id:{self.msisdn}:{self.campaign}", new_job.id)
        redis_conn.set(f"inactivity_report_job:{self.msisdn}:{self.campaign}", inactivity_report_job.id)
        # self.wtsapp_client.send_typing_on(phone_number=self.msisdn)
        self.wtsapp_client.wa_readed(wamid=whatsapp_id)


    def step_completed(self):
        self.next_state()
        self.data.set_state(self.msisdn, self.campaign, self.state, self.now_)
        scheduler.add_job(self.data.odoo_update_state, 'date', run_date=None, args=[self.msisdn, self.campaign, self.state])


    def set_grammar_score_wrapper(self, score: dict) -> None:
        odoo_message.set_grammar_score(score)

    
    def set_pronun_score_wrapper(self, score: dict) -> None:
        odoo_message.set_pronunciation_score(score)


    def validate_grammar(self, text: str):
        #TODO: evaluate grammar here!
        proba, p_max =  self.grammar_probas_scores(text=text)
        score = {
            "msisdn": self.msisdn,
            "a1_score": proba['A1'] * 100,
            "a2_score": proba['A2'] * 100,
            "b1_score": proba['B1'] * 100,
            "b2_score": proba['B2'] * 100,
            "c1_score": proba['C1'] * 100,
            "c2_score": proba['C2'] * 100,
        }
        scheduler.add_job(self.set_grammar_score_wrapper, 'date', run_date=None, args=[score])

    
    def validate_pronunciation(self, text: str):
        # proba, p_max =  self.grammar_probas_scores(text=text)
        score = {
            "msisdn": self.msisdn,
            "cefr_score": "A",
            "pronun_c": "B",
            "fluent_c": "C",
            "vocab_c": "D",
            "gramm_c": "E",
            "pronun": 0.89,
            "fluent": 0.34,
            "vocab": 0.36,
            "gramm": 0.64,

        }
        scheduler.add_job(self.set_grammar_score_wrapper, 'date', run_date=None, args=[score])


   


    @property
    def chat_history(self) -> List[str]:
        collected = self.data.get_collected_messages(self.msisdn, self.campaign)
        chat_history = [f"{c['source']}: {c['message']}" for c in collected]
        return chat_history[:-1]
    


class DataManager():
    def __init__(self) -> None:
        pass

    @property
    def now_(self):
        return datetime.now().astimezone()

    def data_mem_loader(self):
        db = SessionLocal()
        records = db.query(ChatHistory).all()
        for record in records:
            self.add_chat_history(record.msisdn, record.campaign, record.message, record.source, record.whatsapp_id, record.sending_date, record.readed, record.collected) # .isoformat()

        states = db.query(VAStage).all()
        for s in states:
            self.set_state(s.msisdn, s.campaign, s.state, s.last_update)

        db.close()
        print('⚡️ Data in-memory loaded')


    def get_latest_message(self, msisdn: str, campaign: str):
        sorted_set_key = f"{msisdn}:{campaign}"
        # Get the most recent record ID from the sorted set
        latest_record_id = redis_conn.zrevrange(sorted_set_key, 0, 0)
        if latest_record_id:
            latest_record_id = latest_record_id[0].decode('utf-8')
            record_hash_key = f"record:{latest_record_id}"
            # Retrieve the record from the hash
            latest_record = redis_conn.hgetall(record_hash_key)
            # Convert byte data to string and handle JSON conversion
            latest_record = {k.decode('utf-8'): v.decode('utf-8') for k, v in latest_record.items()}
            latest_record['sending_date'] = datetime.fromisoformat(latest_record['sending_date']).astimezone()
            latest_record['readed'] = latest_record['readed'] == '1'
            latest_record['collected'] = latest_record['collected'] == '1'
            return latest_record
        return None
    

    def get_unreaded_messages(self, msisdn: str, campaign: str) -> List[Dict]:
        sorted_set_key = f"{msisdn}:{campaign}"
        unreaded_messages = []
        # Get all record IDs from the sorted set
        record_ids = redis_conn.zrange(sorted_set_key, 0, -1)

        for record_id in record_ids:
            record_hash_key = f"record:{record_id.decode('utf-8')}"
            record = redis_conn.hgetall(record_hash_key)
            # Check if the record is unread
            if int(record.get(b'readed', 1)) == 0:
                # Convert bytes to string
                record = {key.decode('utf-8'): value.decode('utf-8') for key, value in record.items()}
                unreaded_messages.append(record)
        self.mark_as_read(msisdn, campaign)
        # mark_as_read_db(msisdn, campaign)
        scheduler.add_job(self.mark_as_read_db, 'date', run_date=None, args=[msisdn, campaign])
        return unreaded_messages
    

    def get_collected_messages(self, msisdn: str, campaign: str) -> List[Dict]:
        sorted_set_key = f"{msisdn}:{campaign}"
        collected_messages = []
        # Get all record IDs from the sorted set
        record_ids = redis_conn.zrange(sorted_set_key, 0, -1)
        for record_id in record_ids:
            record_hash_key = f"record:{record_id.decode('utf-8')}"
            record = redis_conn.hgetall(record_hash_key)
            if int(record.get(b'collected', 1)) == 1:
                # Convert bytes to string
                record = {key.decode('utf-8'): value.decode('utf-8') for key, value in record.items()}
                collected_messages.append(record)
        return collected_messages
    

    def update_collected(self, unread_messages: List[Dict]):
        last_unread_message = unread_messages[-1]
        sending_date_dt = datetime.fromisoformat(last_unread_message['sending_date'])
        record_id = f"{last_unread_message['msisdn']}:{last_unread_message['campaign']}:{sending_date_dt.timestamp()}"
        record_hash_key = f"record:{record_id}"
        # print(record_hash_key)
        # Update collected status in Redis
        redis_conn.hset(record_hash_key, "collected", 1)
        scheduler.add_job(self.updated_collected_db, 'date', run_date=None, args=[last_unread_message, sending_date_dt])

    def updated_collected_db(self, last_unread_message: dict, sending_date_dt: datetime):
        session = SessionLocal()
        try:
            session.query(ChatHistory).filter(
                ChatHistory.msisdn == last_unread_message['msisdn'],
                ChatHistory.campaign == last_unread_message['campaign'],
                ChatHistory.sending_date == sending_date_dt
            ).update({"collected": True})
            session.commit()
        except Exception as e:
            session.rollback()
            print("Error updating collected status in PostgreSQL:", e)
        finally:
            session.close()


    def mark_as_read(self, msisdn: str, campaign: str):
        sorted_set_key = f"{msisdn}:{campaign}"
        # Get all record IDs from the sorted set
        record_ids = redis_conn.zrange(sorted_set_key, 0, -1)
        for record_id in record_ids:
            record_hash_key = f"record:{record_id.decode('utf-8')}"
            redis_conn.hset(record_hash_key, "readed", 1)


    def mark_as_read_db(self, msisdn: str, campaign: str):
        db = SessionLocal()
        try:
            # Update the readed status to True for all matching records
            db.query(ChatHistory).filter(ChatHistory.msisdn == msisdn, ChatHistory.campaign == campaign).update({"readed": True})
            db.commit()
            # print(f"Updated readed status to True for msisdn: {msisdn}, campaign: {campaign}")
        except Exception as e:
            db.rollback()
            print("Error updating readed status:", e)
        finally:
            db.close()


    def add_chat_history(self, msisdn: str, campaign: str, message: str, source: str, whatsapp_id: str, sending_date: datetime, readed: bool = False, collected: bool = False):
        record = {
            "msisdn": msisdn,
            "campaign": campaign,
            "message": message.replace("\n", ". "),
            "source": source,
            "whatsapp_id": whatsapp_id,
            "sending_date": sending_date.isoformat(),
            "readed": int(readed),
            "collected": int(collected)
        }
        record_id = f"{msisdn}:{campaign}:{sending_date.timestamp()}"
        record_hash_key = f"record:{record_id}"

        # Store the record as a hash
        redis_conn.hset(record_hash_key, mapping=record)
        
        # Store the record ID in a sorted set with the timestamp as the score
        sorted_set_key = f"{msisdn}:{campaign}"
        redis_conn.zadd(sorted_set_key, {record_id: sending_date.timestamp()})


    def add_chat_history_db(self, msisdn: str, campaign: str, message: str, source: str, whatsapp_id: str, sending_date: datetime, readed: bool = False, collected: bool = False):
        db = SessionLocal()
        chat_record = ChatHistory(
            msisdn=msisdn,
            message=message,
            campaign=campaign,
            source=source,
            whatsapp_id=whatsapp_id,
            sending_date=sending_date,
            readed=readed,
            collected=collected
        )
        db.add(chat_record)
        db.commit()
        db.refresh(chat_record)
        db.close()


    def get_state(self, msisdn: str, campaign: str) -> dict:
        state = self.get_mem_state(msisdn, campaign)
        if len(state) == 0:
            db = SessionLocal()
            va_stage = db.query(VAStage).filter_by(msisdn=msisdn, campaign=campaign).first()
            if va_stage is None:
                va_stage = VAStage(msisdn=msisdn, campaign=campaign, state=DEFAULT_STATE, last_update=self.now_)
                db.add(va_stage)
                db.commit()
                db.refresh(va_stage)
                db.close()
            self.set_state(va_stage.msisdn, va_stage.campaign, va_stage.state, va_stage.last_update)
            state = self.get_mem_state(msisdn, campaign)
        return state

    
    def set_state(self, msisdn: str, campaign: str, state: str, last_update: datetime) -> None:
        record = {
            "msisdn": msisdn,
            "campaign": campaign,
            "state": state,
            "last_update": last_update.isoformat(),
        }
        record_id = f"{msisdn}:{campaign}"
        record_hash_key = f"state:{record_id}"
        # Store the record as a hash
        redis_conn.hset(record_hash_key, mapping=record)


    def get_mem_state(self, msisdn: str, campaign: str) -> dict:
        record_id = f"{msisdn}:{campaign}"
        record_hash_key = f"state:{record_id}"
        record = redis_conn.hgetall(record_hash_key)
        return {key.decode(): value.decode() for key, value in record.items()}
    

    def odoo_update_state(self, msisdn: str, campaign: str, state: str):
        if state in ["new", "recording", "evaluation"]:
            odoo_message.applicant_stage(state, msisdn)
        odoo_message.update_stage({
            'msisdn': msisdn,
            'campaign': campaign,
            'state': state,
        })



if __name__ == "__main__":
    import uuid

    wtsapp_client = WhatsAppClient(debug=True)
    machine = SchedulerMachine(msisdn="18296456177", campaign="BOTPROS",  wtsapp_client=wtsapp_client)
    # import os
    # os.system('clear')
    while True:
        text = input("🥸 ")
        if text.lower() == "quit": break
        machine(text, str(uuid.uuid4()))

    redis_conn.flushdb()
