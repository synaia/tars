import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field
from typing import List
from transitions import Machine
from dotenv import dotenv_values
from rich import print


secret = dotenv_values('../../.secret')
llm  = dspy.OpenAI(
    model='gpt-3.5-turbo-0125',
    # model='gpt-3.5-turbo',
    # model='gpt-4',
    # model='gpt-4o',
    api_key=secret['OPEN_AI_API_KEY'],
    max_tokens=4096
)

dspy.settings.configure(lm=llm)

# groq = dspy.GROQ(model='llama3-70b-8192', api_key=secret['GROQ_API_KEY'], max_tokens=2000)
# dspy.settings.configure(lm=groq, )


# Produce key-pair semantic synth-data by stage
# stage: intro + uttetance type == greeting


greetings = {
  "hello_messages": [
    "Hi, how's it going?",
    "Hey! 👋",
    "Hi! I'm excited to chat with you.",
    "Hello! What's up?",
    "Hey there! 😊",
    "Hi, it's nice to meet you.",
    "Hey, how are you today?",
    "Hi! I'm looking forward to talking to you.",
    "Hey! What's new with you?",
    "Hi, how's your day going?",
    "Hey! I'm happy to connect with you.",
    "Hi! It's great to meet you.",
    "Hey, what brings you here?",
    "Hi! I'm excited to get to know you.",
    "Hey! Long time no talk!",
    "Hi! I'm looking forward to chatting with you.",
    "Hey! How's life treating you?",
    "Hi! Let's catch up.",
    "Hey! What's on your mind?",
    "Hi! It's nice to reconnect.",
    "Hey! Let's talk soon.",
    "Hi! I'm glad we connected."
  ]
}


company_related = {
    "comments": [
        "What is the company culture like?",
        "I'm interested in the customer service role, can you send me more info?",
        "Do you offer any training programs for new hires?",
        "What are the working hours for the inbound sales team?",
        "How many days off do we get per year? 🤔",
        "Is there opportunity for growth within the company?",
        "What kind of benefits do you offer to employees?",
        "I'm interested in the data entry role, what are the responsibilities?",
        "Do you have a referral program for employees?",
        "What is the average salary for a customer service rep?",
        "Do you have a dress code policy?",
        "How does the performance evaluation process work?",
        "What kind of support does the company offer for professional development?",
        "Can you tell me more about the team I'll be working with?",
        "What are the company's short-term and long-term goals?",
        "Are there any opportunities for remote work?",
        "What's the typical career path for someone in the customer service team?",
        "Do you offer any employee discounts or perks?",
        "How does the company approach work-life balance?",
        "What sets this company apart from other call centers?",
        "What's the company's policy on flexible scheduling?"
    ]
}


continue_related = {
    "responses": [
	    "Sounds good! Let's move forward.",
	    "I'm happy to help. Please proceed.",
	    "That's correct! Let's continue 💬",
	    "Got it! Next steps are...",
	    "Affirmative, let's go ahead.",
	    "Excellent, what's the next question?",
	    "That's okay, let's try again.",
	    "I completely agree. What's next?",
	    "That's correct! 👍",
	    "I'm on the same page. Please proceed.",
	    "That's awesome! What's the next step?",
	    "I'm excited to see what's next!",
	    "That sounds like a plan. Let's do it.",
	    "I'm with you on that. What's next?",
	    "That's a great idea! Let's run with it.",
	    "That's a good point. Let's build on that.",
	    "I'm good with that. What's the next move?",
	    "That's the right approach. Let's continue.",
	    "That's a great start! What's next?",
	    "I'm on board with that. Let's proceed.",
	    "That's a fantastic idea! Let's make it happen.",
	    "Oki",
	    "Okay",
	    "Ok"
    ]
}


later_continue = {
    "phrases": [
        "I'm taking a break, talk to you later on WhatsApp!",
        "I need to go, catch you later!",
        "I'm feeling a bit tired, will continue this convo later 😴",
        "I'm out for now, will get back to you later!",
        "Have to run, talk to you soon!",
        "I'm not feeling up to chat right now, will continue later",
        "I'm stepping away for a bit, be back soon!",
        "I'm bored with this convo, will catch you later",
        "I have to go, but we can pick this up later",
        "I'm not able to continue right now, will talk to you later",
        "I need some time to myself, talk to you later!",
        "I'm taking a time-out, will come back to this later",
        "I'm not feeling the energy to chat, will catch you later",
        "I have to go, but we can continue this on WhatsApp later",
        "I'm disconnecting for now, talk to you soon!",
        "I'm not able to focus, will pick this up later",
        "I'm out of energy, will catch you later!",
        "I need a break from this convo, will continue later",
        "I'm stepping away, but we can continue this on WhatsApp later",
        "I'm not able to chat right now, will talk to you soon!",
        "I'm feeling drained, will continue this later"
    ]
}


feedbacks = {
    "feedback_requests": [
        "Can you please update me on my application status?",
        "What's the current stage of my hiring process?",
        "Feedback on my interview would be appreciated, thanks!",
        "How's my application doing? 🤔",
        "Any news on my job application?",
        "Could you share an update on my candidacy?",
        "What's the latest on my application?",
        "Kindly inform me about my application progress.",
        "Can I get an update on my interview?",
        "I'd love to know where I stand in the process.",
        "Is there any update on my application status?",
        "Please let me know if I'm still in the running?",
        "Can you give me some feedback on my resume?",
        "What's the current status of my application?",
        "Any feedback on my performance during the interview?",
        "Can I get an update on the hiring process?",
        "I'm eagerly waiting to hear about my application.",
        "What's the decision on my application?",
        "Is my application still being considered?",
        "Am I still in the running for this position?"
    ]
}

def merge_examples(sample_type: str, sample: dict):
    return [dspy.Example({"utterance": f, "utterance_type": sample_type}).with_inputs("utterance") for f in list(sample.values())[0]]

    
examples: List[dspy.Example] = []
all_types = {"greetings": greetings, "company_related": company_related, "continue_related": continue_related, "later_continue": later_continue, "feedbacks": feedbacks}
for sample_type, sample in all_types.items():
    examples.extend(merge_examples(sample_type, sample))

# print(examples)


import random


utterance_type_list = ["greetings", "company_related", "continue_related", "later_continue", "feedbacks", "out_of_scope", "qa_response"]

# help to process providing a stage:
# ej. if stage == 'qa_assestment' then the posibility of utterance_type_list is limited to 
#  company_related, qa_response

class UtteranceClassification(dspy.Signature):
    """A basic utterance classifier in a chat conversation."""
    utterance = dspy.InputField(desc="An user utterance")
    utterance_type = dspy.OutputField(desc=f"One type in the following list {str(utterance_type_list)}")

class UtteranceModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot = dspy.ChainOfThought(UtteranceClassification)

    def forward(self, utterance: str) -> str:
        return self.cot(utterance=utterance)


random_picked: dspy.Example = random.choice(examples)

predictor = UtteranceModule()
response = predictor(utterance=random_picked.utterance)

print(f"Utterance: '{random_picked.utterance}'\npredicted: {response.utterance_type}\nground:    {random_picked.utterance_type}")



from dspy.evaluate import Evaluate
from dspy.evaluate import answer_exact_match


def validate_exact_utterance_type(example, pred, trace=None):
    return example.utterance_type.lower() == pred.utterance_type.lower()


NUM_THREADS = 4
devset = random.sample(examples, 100)
evaluate = Evaluate(devset=devset, metric=validate_exact_utterance_type, num_threads=NUM_THREADS, display_progress=True, display_table=False)
evaluate(predictor, devset=devset)


predictor.load("utterance_module.json")
evaluate(predictor, devset=devset)


