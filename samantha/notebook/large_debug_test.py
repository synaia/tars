import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field
from typing import List
from transitions import Machine
from dotenv import dotenv_values
from rich import print


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
        "Hi! I'm glad we connected.",
        "Hey there! 😊 How's it going?",
        "Good morning! 🌞 Hope you're well!",
        "Hi! 👋 What's up?",
        "Hello! How are you today? 😄",
        "Yo! What's good? 😎",
        "Hey! Long time no chat! 🕰️",
        "Hi! How's everything? 🌟",
        "Hey, what's new? 🤔",
        "Good evening! 🌙 How was your day?",
        "Hey! What's happening? 🤷‍♂️",
        "Hello! How have you been? 😊",
        "Hey, what's cracking? 😄",
        "Hey! How you doin'? 😉",
        "Hello! Trust you're doing well. 🙏",
        "Hi! What's going on? 🤔",
        "Hey, how's your day been? 😊",
        "Greetings! 🎉 How's it going?",
        "Hey! Any news? 📰",
        "Hi there! How's your week been? 📅",
        "Hello! Everything good? 👍",
        "Hey! What's the latest? 📢",
        "Hi! How's your morning? ☕",
        "Hey! What are you up to? 🤔",
        "Hi! How's your day going? 😊",
        "Hello! How are things? 🌟",
        "Hey! How's your night? 🌙",
        "Hi! What's up with you? 🤔",
        "Hey! How's life treating you? 🍀",
        "Hello! How's your week going? 📅",
        "Hi! How's everything on your end? 🌟",
        "Hey! What's good with you? 😎",
        "Hi! How have you been feeling? 😊"
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
        "What's the company's policy on flexible scheduling?",
        "Hey there! Could you tell me more about the company's history?",
        "Good morning! What are the company's main products or services?",
        "Hi! Can you provide some insights into the company culture?",
        "Hello! How does the company foster employee growth and development?",
        "Yo! What's the company's mission and values?",
        "Hey! I'm curious, what sets this company apart from its competitors?",
        "Hi! What's the company's stance on sustainability?",
        "Hey, what's the work environment like at the company?",
        "Hey! What's the company's approach to diversity and inclusion?",
        "Hi! Can you tell me about the company's financial performance?",
        "Hello! How does the company give back to the community?",
        "Hey, what's the average tenure of employees at the company?",
        "Hi! How does the company ensure a safe and inclusive workplace?",
        "Hey! Can you share any upcoming projects or initiatives the company is working on?",
        "Hello! What's the company's policy on remote work?",
        "Hi! How does the company encourage innovation among its employees?",
        "Hey! Can you tell me about the company's customer base?",
        "Hello! What training and development opportunities does the company provide?",
        "Hey, what benefits does the company offer to its employees?",
        "Hey! Can you provide some information about the company's technology stack?",
        "Hello! How does the company ensure data privacy and security?",
        "Hi! What's the company's policy on flexible working hours?",
        "Hey! I'm interested to know about the company's training programs.",
        "Hi! Can you tell me about the company's customer satisfaction ratings?",
        "Hey, what opportunities for professional development does the company offer?",
        "Hello! How does the company celebrate employee achievements?",
        "Hi! What's the company's approach to employee wellness?",
        "Hey! Can you share any success stories or case studies?",
        "Hello! How does the company support employee mental health?",
        "Hi! What's the company's strategy for growth and expansion?",


        "Can you tell me more about the company's culture?",
        "What's the typical career path for someone in this role?",
        "How do you measure success in this position?",
        "What are the main challenges new hires usually face?",
        "Is there room for growth within the company?",
        "What kind of training programs do you offer?",
        "Can you explain the team structure here?",
        "How do you handle employee feedback?",
        "What's the most rewarding part of working here?",
        "What are the shift patterns like?",
        "Do you offer remote working options?",
        "How do you support work-life balance?",
        "What are the next steps in the hiring process?",
        "Can you describe a typical day in this job?",
        "How does this role contribute to the company's goals?",
        "What's the company's stance on overtime?",
        "Do you provide any mental health support for employees?",
        "How often do you conduct performance reviews?",
        "What's the team dynamic like?",
        "Are there opportunities for advancement?",
        "What's the company's turnover rate?",
        "Can you tell me more about the company’s mission?",
        "How does the company recognize and reward outstanding performance?",
        "What are the biggest challenges the company is currently facing?",
        "How do you handle conflict within the team?",
        "What's the onboarding process like?",
        "How are goals and expectations communicated to the team?",
        "What kind of feedback can I expect from my supervisor?",
        "What's your policy on work-from-home?",
        "How diverse is your team?",
        "Are there opportunities for cross-training or job rotation?",
        "What tools and technologies will I be using?",
        "How does the company support professional development?",
        "What's the company’s approach to customer service?",
        "Do you have a mentoring program?",
        "What are the main goals for the team this year?",
        "Can you tell me about a successful project the team has completed recently?",
        "What type of clients or customers does the company serve?",
        "How does the company handle high-stress periods?",
        "What's the most common reason employees stay long-term?",
        "Do you offer any tuition reimbursement programs?",
        "How would you describe the company’s management style?",
        "What are the key skills needed for success in this role?",
        "What are the company's values?",
        "How do you ensure employees feel valued?",
        "Is there a dress code?",
        "How soon can I expect to hear back after this interview?",
        "What are the benefits and perks?",
        "How do you keep employees motivated and engaged?",
        "Do you celebrate achievements or milestones?"
        
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
	    "Ok",
        "Yes, I would like to continue.",
        "Sure, I'm in!",
        "Absolutely, let's go ahead.",
        "Count me in!",
        "I agree, let's proceed.",
        "I'm on board with this.",
        "Yep, sounds good to me.",
        "Definitely, let's do this.",
        "Okay, I'm ready to move forward.",
        "Alright, let's continue.",
        "Of course, I'm in favor.",
        "👍 I'm in.",
        "Yes, please proceed.",
        "I'm all set to continue.",
        "For sure, let's keep going.",
        "I'm okay with that, let's proceed.",
        "Certainly, I agree.",
        "👌 Let's go for it.",
        "Fine by me, let's move forward.",
        "I'm down for this!"
    ]
}


not_continue_related = {
    "responses": [
        "Thanks for the offer, but I’ll pass this time.",
        "I appreciate it, but I’m not interested in continuing.",
        "I'm going to have to decline, thanks for considering me.",
        "Sorry, but I don’t agree with this approach.",
        "I’ve decided not to move forward with this process.",
        "Thanks, but I’m not up for it.",
        "Unfortunately, I have to say no.",
        "I’m not comfortable with this, sorry.",
        "I’m out, but thanks for the opportunity.",
        "I’ve thought about it, and I’m not interested.",
        "Thanks, but this isn't for me.",
        "I'm going to step back from this, but thank you.",
        "I’m choosing not to proceed, thanks.",
        "This doesn't align with my interests, so I’m not continuing.",
        "I’ll be bowing out of this process.",
        "I’m going to pass on this, thanks though.",
        "No, I’m not going to accept this.",
        "I can’t go along with this plan.",
        "I have to say no, but I appreciate it.",
        "Not agreeing with this, sorry.",
        "I’m not interested in pursuing this further.",
        "I’m going to have to pass on this opportunity.",
        "I won’t be moving forward with this, thanks.",
        "This isn’t something I want to do, sorry.",
        "I’m not on board with this.",
        "Nope, not for me. Thanks anyway!",
        "I’m not feeling this, so I’m out.",
        "I’m going to decline, but I appreciate the offer.",
        "This doesn’t work for me, so I’m saying no.",
        "I’ve decided against this, thanks anyway.",
        "I’m not continuing with this, sorry.",
        "I’m declining to move forward, thanks.",
        "Thanks, but I’ll have to decline.",
        "This isn't the right fit for me, so no.",
        "I don't agree with this, so I won't proceed.",
        "I’m going to have to say no to this.",
        "Sorry, but I’m not interested in this.",
        "Thanks, but I’m not going ahead with this.",
        "I’m passing on this, but thanks.",
        "I’m choosing not to participate, thank you."
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
        "I'm feeling drained, will continue this later",
        "Hey there! Thanks for reaching out. I'm currently tied up with a meeting, can we continue this later?",
        "Good morning! I'm in the middle of something right now, can we pick this up in an hour?",
        "Hi! Sorry, I'm swamped at the moment. Can we chat about this tomorrow?",
        "Hello! I'm unable to continue the process at the moment due to some unforeseen circumstances.",
        "Yo! Can we put a pin on this for now? I'll get back to you as soon as I can.",
        "Hey! Unfortunately, I won't be able to proceed further with the interview today. Can we reschedule?",
        "Hi! I'm tied up with back-to-back meetings. Can we touch base later?",
        "Hello! I'm currently on the go, so I'll have to get back to you about this later.",
        "Hey there! I'm really sorry, but I have an urgent task to attend to. Can we resume this discussion tomorrow?",
        "Good morning! I'm running a bit behind schedule today. Can we continue this conversation later?",
        "Hi! I'm afraid I won't be able to proceed with the evaluation at the moment. Can we reconvene tomorrow?",
        "Hello! I'm currently dealing with an emergency situation. Can we postpone this to a later time?",
        "Hey! I'm really sorry, but I have to step away for a moment. Can we continue this in an hour?",
        "Hi! Unfortunately, I've hit a roadblock in the process. Can we revisit this tomorrow?",
        "Hey there! I'm in the middle of something important. Can we catch up on this later?",
        "Hello! I'm sorry, but I'm unable to dedicate time to this right now. Can we discuss this tomorrow?",
        "Hi! I'm currently occupied with a pressing matter. Can we pick this up later in the day?",
        "Hey! I'm juggling multiple tasks at the moment. Can we continue this at a more convenient time?",
        "Hi! I'm really sorry, but I have to step out unexpectedly. Can we continue this discussion later?",
        "Hello! I'm tied up with a deadline right now. Can we revisit this tomorrow?"
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
        "Am I still in the running for this position?",
        "Hey there! Just checking in to see if there's any update on my interview status?",
        "Good morning! I was wondering if there's any news on where I stand in the evaluation process.",
        "Hi! Can you provide me with an update on the status of my application, please?",
        "Hello! I hope you're doing well. Could you please let me know the current status of my interview?",
        "Yo! Any chance I could get an update on how things are progressing with my evaluation?",
        "Hey! Just wanted to touch base and inquire about the status of my application.",
        "Hi! I hope all is going smoothly. Any updates on my interview status?",
        "Hello! Hope you're having a great day. Can you give me an update on my evaluation status?",
        "Hey there! Wondering if there's any news on my application status?",
        "Good morning! I hope you're doing well. Could you provide me with an update on my interview status?",
        "Hi! Just checking in to see if there's any progress with my evaluation.",
        "Hello! Hope you're having a good day. Any updates on my interview status?",
        "Hey! Any chance I could get an update on my application status?",
        "Hi! I hope you're doing well. Can you please let me know the status of my evaluation?",
        "Hello! Just reaching out to see if there's any update on my interview status.",
        "Hey there! Hoping to get an update on my application status.",
        "Hi! I'm eager to know the status of my evaluation. Any updates?",
        "Hello! Can you please provide me with an update on my interview status?",
        "Hey! Just wanted to follow up on my application status. Any news?",
        "Hi! I hope all is going smoothly. Could you provide me with an update on my evaluation status, please?"
    ]
}


qa_1 = {
    "qa_1_responses":  [
        "Sure, I have 3 years of experience working in a call center, handling customer inquiries and resolving issues efficiently.",
        "Absolutely! I used to work in customer support for a tech company, helping clients with troubleshooting and product information.",
        "Hey there! I spent 2 years at a call center, where I honed my skills in customer service and communication.",
        "I've been in customer service for about 4 years now, mostly dealing with billing issues and service upgrades.",
        "Yes, I worked as a customer service representative at a retail company, assisting customers with their orders and returns.",
        "For sure! I have experience in a call center environment where I dealt with high-volume calls and customer complaints.",
        "I used to handle customer queries and technical support for an ISP. It was challenging but rewarding!",
        "Worked at a call center for 2 years, helping customers with account setups and troubleshooting issues.",
        "Totally! My last job was in a call center, where I assisted customers with their service-related concerns.",
        "Yes, I have experience in customer service, including resolving disputes and ensuring customer satisfaction.",
        "Sure thing! I was a customer service agent at a financial institution, helping clients with their account management.",
        "I’ve been in customer service roles for the past 5 years, focusing on resolving customer issues and enhancing their experience.",
        "Definitely! I worked in a call center where I handled escalated calls and provided solutions to complex problems.",
        "Yeah, I've got experience in customer service, mainly working in a support center for a telecom company.",
        "I worked in a call center for 3 years, dealing with various customer issues and providing tech support.",
        "In my previous job, I was responsible for managing customer inquiries and complaints in a busy call center.",
        "Yes, I have a background in customer service, having worked in a call center environment for a couple of years.",
        "I’ve done customer service for a software company, where I helped users with troubleshooting and product guidance.",
        "My experience includes working in a call center where I provided assistance with billing, technical issues, and general inquiries.",
        "👋 I've worked in customer service for 2 years, focusing on resolving customer issues and ensuring their satisfaction."
    ]
}


qa_2 = {
    "qa_2_responses":  [
        "I stay motivated by taking short breaks and listening to my favorite music.",
        "Keeping a positive mindset and thinking about the happy customers I've helped keeps me going.",
        "I remind myself of my goals and the rewards of hard work.",
        "I take deep breaths and focus on one task at a time.",
        "Honestly, a cup of strong coffee and some good vibes do the trick! ☕️✨",
        "I stay energized by keeping a picture of my family on my desk.",
        "Motivation comes from knowing I make a difference in someone's day.",
        "Staying organized and having a plan helps me stay on track.",
        "I chat with my coworkers and share a laugh when things get tough.",
        "I keep motivated by setting small, achievable goals throughout the day.",
        "I think about the end of the day and the satisfaction of a job well done.",
        "I stay positive by celebrating little victories and milestones.",
        "I listen to motivational podcasts during my breaks.",
        "Remembering why I started this job in the first place helps a lot.",
        "I keep a stash of my favorite snacks for a quick energy boost. 🍫",
        "I stay focused by visualizing my career growth and future opportunities.",
        "I find motivation in the supportive team and positive work environment.",
        "Taking a moment to stretch and move around helps keep me energized.",
        "I love hearing feedback from satisfied customers, it really lifts my spirits.",
        "I remind myself that each call is a chance to learn something new."
    ]
}


qa_3 = {
    "qa_3_responses":  [
        "I always stay calm and listen to the customer's concerns carefully before offering a solution.",
        "It's all about empathy and understanding their point of view, then finding a way to make things right.",
        "First, I try to understand the problem from their perspective and then work towards a satisfactory resolution.",
        "I usually take a deep breath, remain composed, and ensure the customer feels heard and valued.",
        "I focus on active listening and try to resolve their issues promptly to keep them satisfied.",
        "Handling tough situations involves staying positive, being patient, and finding effective solutions.",
        "I make sure to acknowledge their frustration and then offer a step-by-step solution.",
        "Gotta keep cool, listen up, and sort out their issue as best as I can.",
        "First things first, I let them vent and then work on resolving their problem efficiently.",
        "Staying calm and collected, I address their concerns and provide a swift resolution.",
        "I ensure to empathize with them and address their issues in a professional manner.",
        "Listening actively and offering practical solutions is my go-to approach.",
        "I keep my cool and always make sure the customer feels understood and appreciated.",
        "I apologize for any inconvenience caused and work diligently to fix the issue.",
        "I stay patient and offer solutions that are both effective and timely.",
        "My approach is to stay calm, understand their problem, and resolve it ASAP. 👍",
        "I believe in listening carefully and addressing their concerns with empathy and efficiency.",
        "I let them know I'm here to help and then provide a solution that meets their needs.",
        "Handling it with a smile and a can-do attitude usually helps in resolving their issues. 😊",
        "I stay professional, listen to their problems, and work towards a quick resolution."
    ]
}


qa_4 = {
    "qa4_responses": [
        "Hey! Absolutely, I thrive in team settings and have no problem following established procedures.",
        "Sure thing! I'm great at collaborating with others and sticking to company policies.",
        "Yep, I'm a team player and always follow the rules and procedures.",
        "Definitely! I work well with others and adhere to established policies and procedures.",
        "Of course! I'm all about teamwork and making sure everything runs smoothly according to the rules.",
        "No doubt! I excel in team environments and am diligent about following policies and procedures.",
        "Absolutely! Working in a team is my jam, and I'm all about following the rules.",
        "You bet! Teamwork is key, and I'm committed to following established policies and procedures.",
        "Yes, I'm quite comfortable working in a team and following all the necessary procedures.",
        "Yep, team player here! I'm good at working collaboratively and sticking to procedures.",
        "For sure! I'm a team player through and through, and I'm diligent about following policies and procedures.",
        "Absolutely! I thrive in team environments and am committed to following all policies and procedures.",
        "Definitely! Teamwork is my forte, and I'm dedicated to following established policies and procedures.",
        "Sure thing! I'm all about teamwork and ensuring everything is done according to the rules.",
        "Of course! I'm comfortable working in a team and following all procedures.",
        "No problem at all! I'm great at collaborating with others and adhering to policies and procedures.",
        "Absolutely! I'm a team player, and I take following policies and procedures seriously.",
        "Yep, teamwork is my specialty! I'm good at following established procedures.",
        "You got it! I work effectively in team environments and always stick to the policies and procedures.",
        "Yes, indeed! I'm quite adept at working in teams and following all necessary procedures."
    ]
}

def merge_examples(sample_type: str, sample: dict):
    return [dspy.Example({"utterance": f, "utterance_type": sample_type}).with_inputs("utterance") for f in list(sample.values())[0]]

    
examples: List[dspy.Example] = []
all_types = {
    "greetings": greetings,
    "company_related": company_related, 
    "continue_related": continue_related,
    "not_continue_related": not_continue_related,
    "later_continue": later_continue, 
    "feedbacks": feedbacks, 
    "qa_1": qa_1,
    "qa_2": qa_2,
    "qa_3": qa_3,
    "qa_4": qa_4,
}
for sample_type, sample in all_types.items():
    examples.extend(merge_examples(sample_type, sample))

print(len(examples))



import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

tokenizer_embed = AutoTokenizer.from_pretrained('bert-base-uncased')
model_embed = AutoModel.from_pretrained('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True, safe_serialization=True)
model_embed.eval()

def embedd(text: str):
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    encoded_input = tokenizer_embed(text, padding=True, truncation=True, return_tensors='pt')
    # + matryoshka_dim = 512
    with torch.no_grad():
        model_output = model_embed(**encoded_input)

    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    # + embeddings = F.layer_norm(embeddings, normalized_shape=(embeddings.shape[1],))
    # + embeddings = embeddings[:, :matryoshka_dim]
    embeddings = F.normalize(embeddings, p=2, dim=1)
    return np.array(embeddings)[0]


import random
from transitions import Machine
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
import dspy
from dspy.functional import TypedPredictor
from dspy.retrieve.pgvector_rm import PgVectorRM
from pydantic import BaseModel, Field
from typing import List
from transitions import Machine
from dotenv import dotenv_values
from rich import print


db_url = "postgresql://drfadul:dROG%40dijoFadul@localhost/synaia"
retriever_model = PgVectorRM(
    db_url=db_url, 
    pg_table_name="company_info",
    k=3,
    embedding_func=embedd,
    embedding_field="embedding",
    fields=["text"],
    include_similarity=True
)

MESSAGES = [] # TODO: It can be a conversation history from a database.
MEM_SIZE = 8
secret = dotenv_values('.secret')

openai  = dspy.OpenAI(
    model='gpt-3.5-turbo-0125',
    # model='gpt-3.5-turbo',
    # model='gpt-4',
    # model='gpt-4o',
    api_key=secret['OPEN_AI_API_KEY'],
    max_tokens=4096,
    model_type="chat",
)
dspy.settings.configure(lm=openai)


class NotFound(dspy.Signature):
    """Generates a denial response related to the question in context"""
    context: str = dspy.InputField()
    response: str = dspy.OutputField(desc="often between 3 and 7 words")


class Veracity(dspy.Signature):
    context_provided: str = dspy.InputField(desc="may contain relevant facts")
    answer: str = dspy.InputField()
    answer_is_in_context_provided: bool = dspy.OutputField(desc="verify that the answer is in the context_provided, respond True or False")


class CompanySignature(dspy.Signature):
    """Answer questions with short factoid answers and friendly, use emoji. Answer should be in the context."""
    context: str = dspy.InputField(desc="may contain relevant facts")
    question: str = dspy.InputField(desc="user question to be answered")
    answer: str = dspy.OutputField(desc="often between 6 and 12 words")


class CompanyRelated(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retriever = retriever_model
        self.predict = dspy.ChainOfThought(CompanySignature)
        self.veracity = dspy.TypedChainOfThought(Veracity)
        self.not_found = dspy.Predict(NotFound)
    
    def forward(self, question: str):
        context = self.retriever(question)
        context = [ctx['text'] for ctx in context]
        response = self.predict(context=context, question=question)
        veracity = self.veracity(context_provided=str(context), answer=response.answer)
        if veracity.answer_is_in_context_provided:
            r = response
            return {
                "answer": r.answer,
                "answer_is_in_context_provided": veracity.answer_is_in_context_provided
            }
        else:
            r = self.not_found(context=question)
            return {
                "answer": r.response,
                "answer_is_in_context_provided": veracity.answer_is_in_context_provided
            }
        

class AnswerComment(dspy.Signature):
    """Generate a positive or supportive comment to the response, use emoji."""
    response: str = dspy.InputField()
    comment: str = dspy.OutputField(desc="often between 5 and 10 words")

        

utterance_type_list = list(all_types.keys())
utterance_type_list.append('out_of_scope')

class UtteranceSignature(dspy.Signature):
    """A basic utterance classifier in a chat conversation."""
    utterance = dspy.InputField(desc="An user utterance")
    utterance_type = dspy.OutputField(desc=f"One type in the following list {str(utterance_type_list)}")


class UtteranceClassificator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot = dspy.ChainOfThought(UtteranceSignature)

    def forward(self, utterance: str) -> str:
        kwargs = {"__memorize": False}
        return self.cot(utterance=utterance)
    

class ActionSignature(dspy.Signature):
    """A basic notification"""
    utterance = dspy.InputField(desc="An user utterance")
    response = dspy.OutputField()

    
class Action(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.action_push = dspy.ChainOfThought(signature)
        
    def forward(self, utterance: str):
        return self.action_push(utterance=utterance)
    


class Stages(Machine):
    def __init__(self, initial_state: str = 'new',) -> None:
        states = ["new", "question_1", "question_2", "question_3", "question_4", "recording", "evaluation"]
        self.utt_clasificator = UtteranceClassificator()
        self.utt_clasificator.load("samantha/notebook/utterance_module_v2.json")
        self.utterance = ""
        self.response: str = ""

        self.company_related_module = CompanyRelated()
        self.answer_comment = dspy.ChainOfThought(AnswerComment)

        Machine.__init__(self, states=states, initial=initial_state)
        self.add_transition(trigger='greetings', source='*', dest=None, prepare=self.move)
        self.add_transition(trigger='continue_related', source='*', dest=None, prepare=self.move)
        self.add_transition(trigger='later_continue', source='*', dest=None, prepare=self.later)
        self.add_transition(trigger='not_continue_related', source='*', dest=None, prepare=self.later)
        self.add_transition(trigger='company_related', source='*', dest=None, prepare=self.company)
        self.add_transition(trigger='feedbacks', source='*', dest=None, prepare=self.feedback)
        self.add_transition(trigger='out_of_scope', source='*', dest=None, prepare=self.outofscope)
        self.add_transition(trigger='qa_1', source=['question_1', 'question_2', 'question_3', 'question_4'], dest=None, prepare=self.qa)
        self.add_transition(trigger='qa_2', source=['question_1', 'question_2', 'question_3', 'question_4'], dest=None, prepare=self.qa)
        self.add_transition(trigger='qa_3', source=['question_1', 'question_2', 'question_3', 'question_4'], dest=None, prepare=self.qa)
        self.add_transition(trigger='qa_4', source=['question_1', 'question_2', 'question_3', 'question_4'], dest=None, prepare=self.qa)

        self.add_ordered_transitions()

        #TODO: continuar aqui .....
        self.question_list = [
            {'question_1': 'What is your previous experience in customer service or in a call center environment?'},
            {'question_2': 'How do you stay motivated during long hours of customer service?'},
            {'question_3': ''},
            {'question_4': ''},
        ]

        self.signature_map = {
            'greetings': {
                '_signature': 'Back hello as a response acording to the context information. ',
                'new': 'Ask the following question: What is your previous experience in customer service or in a call center environment?',
                'question_1': 'tell the user to answer the question question_1.',
                'question_2': 'tell the user to answer the question question_2.',
                'question_3': 'tell the user to answer the question question_3.',
                'question_4': 'tell the user to answer the question question_4.',
                'recording':'Ask if is ready to continue with the recording step.',
            },
            'continue_related': {
                '_signature': '',
                'new': 'Ask the following question: What is your previous experience in customer service or in a call center environment?',
                'qa_1': 'Ask the following question: How do you stay motivated during long hours of customer service?',
                'qa_2': 'Answer the following: now can we start recording your voice?',
                'recording': 'You should thank him or her for participating.',
            },
            'not_continue_related': {
                '_signature': 'Reply we appreciate your time, If you change your mind, we will be gladly waiting for you. ',
            },
            'later_continue': {
                '_signature': 'Reply we appreciate your time, it will only take a minute or two, if you can\'t yet, when can I write to you? ',
            },
            'company_related': {
                '_signature': 'Answer this company question probably using RAG. ',
            },
            'feedbacks': {
                '_signature': 'Answer this user feedback question probably hitting the data base. ',
            },
            'out_of_scope': {
                '_signature': 'Respond by saying that is not within your power and why don\'t we go back to the prescreening process! ',
            },
            'qa_1': {
                '_signature': 'question_1, Is it a valid answer according to the question "{}" ? ',
            },
            'qa_2': {
                '_signature': 'question_2, Is it a valid answer according to the question "{}" ? ',
            },
            'qa_3': {
                '_signature': 'question_3, Is it a valid answer according to the question "{}" ? ',
            },
            'qa_4': {
                '_signature': 'question_4, Is it a valid answer according to the question "{}" ? ',
            },
        }

    def router(self, utterance: str):
        self.utterance = utterance
        response = self.utt_clasificator(utterance)
        self.trigger(response.utterance_type, response.utterance_type)

    def _pkg(self, utt_type: str):
        if self.state in self.signature_map[utt_type]:
            state_message = self.signature_map[utt_type][self.state]
        else:
            state_message = ''
        signature = self.signature_map[utt_type]['_signature'] + state_message
        ActionSignature.__doc__ = signature
        action = Action(ActionSignature)
        response = action(utterance=self.utterance)
        self.response = response
        return response


    def push(self, utt_type: str):
        response = self._pkg(utt_type)
        print(response)

    def move(self, utt_type: str):
        response = self._pkg(utt_type)
        #TODO: also move to the next state
        prev = self.state
        if "new" == self.state: self.next_state()
        print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  prev: {prev}  curr: {self.state}")
        print(response)
        if "question" in prev: print('PIN to the last question.')
       

    def later(self, utt_type: str):
        response = self._pkg(utt_type)
        print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  curr: {self.state}")
        print(response)

    def company(self, utt_type: str):
        signature = self.signature_map[utt_type]['_signature'] #TODO: not used
        print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  curr: {self.state}")
        response = self.company_related_module(question=self.utterance)
        print(response)
        if "question" in self.state: print('Ask to response the last question or TASK (recording), PIN to the last question.')

    def feedback(self, utt_type: str):
        #TODO: use ReACT/retriever and query in DB relevant user information status.
        signature = self.signature_map[utt_type]['_signature']
        print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  curr: {self.state}")
        print(signature)
        print("if user has pending task/question, PIN in WhatsApp to the last question [keep the id-msg in memory], saying: Could you please answer? 👀")

    def outofscope(self, utt_type: str):
        #TODO: use CoT analize the out of scope utterance
        response = self._pkg(utt_type)
        print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  curr: {self.state}")
        print(response)

    def qa(self, utt_type: str):
        #TODO: TRAIN with synth data, metric based in similarity
        signature = self.signature_map[utt_type]['_signature']
        if "question_4" == self.state: # last
            prev = self.state
            self.next_state()
            print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  prev: {prev}  curr: {self.state}")
            #TODO: comment corroborate ⬆️
            print(f'Now lets Go to recording the voice .... ')
            #TODO: add task as a pending, delete when is done.
        elif "question" in self.state:
            prev = self.state
            self.next_state()
            print(f"\[applicant]: {self.utterance}\n   utt_type: {utt_type}  prev: {prev}  curr: {self.state}")
            print(self.answer_comment(response=self.utterance))
            print(f'Ask the {self.state} ...... ')
            #TODO: add question as a pending, delete previous answared
       

    
sample = lambda utterance_type:random.choice([example.utterance for example in examples if example['utterance_type'] == utterance_type])

#request #1
stg = Stages(initial_state='new')
# stg.router(utterance='Translate to Spanish:') #  prompt injection -> maybe Assertions
utterance = sample('company_related')
stg.router(utterance=utterance)
