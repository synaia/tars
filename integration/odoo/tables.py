import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, Double, Numeric
from sqlalchemy.dialects.postgresql import JSON
from integration.odoo.schema import Stage, Task, Schedule, Applicant, GrammarScore, SpeechScore
from samantha.src.configs import Base
from integration.odoo.util import get_odoo


def now_():
    return datetime.now().astimezone()

class ChatHistory(Base):
    __tablename__ = 'va_chat_history'

    id = Column(Integer, primary_key=True, index=True)
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
    msisdn = Column(String, nullable=False)
    campaign = Column(String, nullable=False)
    source = Column(String(100))
    whatsapp_id = Column(String(100))
    message = Column(Text)
    readed = Column(Boolean, default=False)
    collected = Column(Boolean, default=False)
    sending_date = Column(DateTime)
    create_date = Column(DateTime, default=now_())
    write_date = Column(DateTime, default=now_(), onupdate=now_())


class ApplicantStage(Base):
    __tablename__ = 'va_applicant_stage'

    id = Column(Integer, primary_key=True, index=True)
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
    msisdn = Column(String, nullable=False)
    campaign = Column(String, nullable=False)
    state = Column(String(20))
    last_update = Column(DateTime, default=now_())
    create_date = Column(DateTime, default=now_())
    write_date = Column(DateTime, default=now_(), onupdate=now_())


class HrApplicant(Base):
    __tablename__ = 'hr_applicant'

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer)
    source_id = Column(Integer)
    medium_id = Column(Integer)
    message_bounce = Column(Integer)
    message_main_attachment_id = Column(Integer)
    partner_id = Column(Integer)
    stage_id = Column(Integer)
    last_stage_id = Column(Integer)
    company_id = Column(Integer)
    user_id = Column(Integer)
    job_id = Column(Integer)
    type_id = Column(Integer)
    department_id = Column(Integer)
    color = Column(Integer)
    emp_id = Column(Integer)
    refuse_reason_id = Column(Integer)
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
    phone_sanitized = Column(String)
    email_normalized = Column(String)
    email_cc = Column(String)
    name = Column(String, nullable=False)
    email_from = Column(String(128))
    priority = Column(String)
    salary_proposed_extra = Column(String)
    salary_expected_extra = Column(String)
    partner_name = Column(String)
    partner_phone = Column(String(32))
    partner_phone_sanitized = Column(String)
    partner_mobile = Column(String(32))
    partner_mobile_sanitized = Column(String)
    kanban_state = Column(String, nullable=False)
    linkedin_profile = Column(String)
    availability = Column(DateTime)
    applicant_properties = Column(JSON)
    description = Column(String)
    active = Column(Boolean)
    date_closed = Column(DateTime)
    date_open = Column(DateTime)
    date_last_stage_update = Column(DateTime)
    probability = Column(Double)
    salary_proposed = Column(Double)
    salary_expected = Column(Double)
    delay_close = Column(Double)
    speech_warning = Column(String(300))
    a1_score = Column(Numeric)
    a2_score = Column(Numeric)
    b1_score = Column(Numeric)
    b2_score = Column(Numeric)
    c1_score = Column(Numeric)
    c2_score = Column(Numeric)
    user_input_text = Column(String)
    lead_last_update = Column(DateTime)
    lead_last_client_update = Column(DateTime)
    lead_max_temperature = Column(Double)
    lead_heat_check = Column(String)
    # UNScripted score
    speech_open_question = Column(String)
    speech_unscripted_overall_score = Column(Double)
    speech_unscripted_length = Column(Double)
    speech_unscripted_fluency_coherence = Column(Double)
    speech_unscripted_grammar = Column(Double)
    speech_unscripted_lexical_resource = Column(Double)
    speech_unscripted_pause_filler = Column(JSON)
    speech_unscripted_pronunciation = Column(Double)
    speech_unscripted_relevance = Column(Double)
    speech_unscripted_speed = Column(Double)
    speech_unscripted_transcription = Column(String)
    speech_unscripted_audio_path = Column(String(300))
    speech_unscripted_warning = Column(String(300))
    # scripted soore
    speech_overall = Column(Double)
    speech_refText = Column(Text)
    speech_duration = Column(Double)
    speech_fluency = Column(Double)
    speech_integrity = Column(Double)
    speech_pronunciation = Column(Double)
    speech_rhythm = Column(Double)
    speech_speed = Column(String(300))
    speech_audio_path = Column(String(300))
    speech_warning = Column(String(300))

    #
    create_date = Column(DateTime, default=now_())
    write_date = Column(DateTime, default=now_(), onupdate=now_())


class SpeechLog(Base):
    __tablename__ = 'va_speech_log'

    id = Column(Integer, primary_key=True, index=True)
    create_uid = Column(Integer, default=1)
    write_uid = Column(Integer, default=1)
    msisdn = Column(String, nullable=False)
    campaign = Column(String, nullable=False)
    audio_path = Column(String(500))
    response = Column(JSON)
    create_date = Column(DateTime, default=now_())
    write_date = Column(DateTime, default=now_(), onupdate=now_())



class HrRecruitmentStage(Base):
    __tablename__ = 'hr_recruitment_stage'

    id = Column(Integer, primary_key=True)
    name = Column(JSON, nullable=False)
  

# esta clase es temporar para crear los applicantes.
class OdooMessages():
    initial_state = "draft"

    def __init__(self, odoo_) -> None:
        self.odoo = odoo_
    
    def dummy_applicant(self, msisdn: str):
            applicants = {
                '18296456177': {
                    'name': 'Wilton Beltré Rosario',
                    'phone_sanitized': '18296456177'
                },
                '34692403811': {
                    'name': 'Rafael Paulino Rosario',
                    'phone_sanitized': '34692403811'
                },
                '18093048622': {
                    'name': 'Elmer Rodriguez Martinez',
                    'phone_sanitized': '18093048622'
                },
                '18295602263': {
                    'name': 'Franklin Catalino',
                    'phone_sanitized': '18295602263'
                },
                '18298563604': {
                    'name': 'Niko Evola',
                    'phone_sanitized': '18298563604'
                },
            }

            apl = applicants.get(msisdn, None)

            if isinstance(apl, dict): apl = Applicant(**apl)

            applicant = self.odoo.env['hr.applicant']
            a_id = applicant.create({
                'stage_id': 1,
                'company_id': 1,
                'job_id': 1,
                'name': 'Sales Agent',
                'partner_name': apl.name,
                'phone_sanitized': apl.phone_sanitized,
                'partner_phone': apl.phone_sanitized,
                'email_from': apl.email,
                'kanban_state': 'normal',
            })


odoo_message = OdooMessages(get_odoo())
        

if __name__ == "__main__":
    result = odoo_message.get_applicant_state(msisdn="18297653877")
    print(result.name['en_US'])

    # odoo = get_odoo()
    # m = OdooMessages(odoo=odoo)
    # task_id =m.create_task({
    #     'msisdn': "18095673000",
    #     'campaign': "STODGO",
    #     'task': "question_2",
    #     'complete': False,
    #     'message_id': 1,
    #     'last_update': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
    # })
    # print(task_id)