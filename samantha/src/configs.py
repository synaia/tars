
import logging
import torch 
import dspy
import redis
from transformers import RobertaForSequenceClassification, RobertaTokenizerFast
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
from dspy.retrieve.pgvector_rm import PgVectorRM

from .embedding_model import embedd
from integration.odoo.util import get_odoo
from integration.odoo.va import OdooMessages


secret = dotenv_values('.secret')
db_url = secret['POSTGRES_URL']

retriever_model = PgVectorRM(
    db_url=db_url, 
    pg_table_name="company_info",
    k=3,
    embedding_func=embedd,
    embedding_field="embedding",
    fields=["text"],
    include_similarity=True
)

ASSISTANT_NAME = "Samantha"
system_prompt = f"""You are {ASSISTANT_NAME}, an assistant at a call center recruiting company."""

openai  = dspy.OpenAI(
    model='gpt-3.5-turbo-0125',
    # model='gpt-3.5-turbo',
    # model='gpt-4',
    # model='gpt-4o',
    api_key=secret['OPEN_AI_API_KEY'],
    max_tokens=4096,
    model_type="chat",
    system_prompt=system_prompt
)
dspy.settings.configure(lm=openai)

print('⚡️ LLM loaded')

redis_conn = redis.Redis(host='localhost', port=6379, db=0)
print('⚡️ Redis loaded')

# Configure APScheduler to use Redis as the job store
jobstores = {
    'default': RedisJobStore(host='localhost', port=6379, db=1)
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()
print('⚡️ Scheduler loaded')

# # Setup logging
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.INFO)

log_file = 'scheduler.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

secret = dotenv_values(".secret")

# PostgreSQL setup
DATABASE_URL = secret['POSTGRES_URL']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
print('⚡️ Postgres loaded')

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    msisdn = Column(String, index=True)
    campaign = Column(String, index=True)
    message = Column(Text)
    source = Column(Text)
    whatsapp_id = Column(String, index=True)
    sending_date = Column(DateTime)
    readed = Column(Boolean)
    collected = Column(Boolean)


class VAStage(Base):
    __tablename__ = "va_stage"
    id = Column(Integer, primary_key=True, index=True)
    msisdn = Column(String, index=True)
    campaign = Column(String, index=True)
    state = Column(String)
    last_update = Column(DateTime)
    

def get_device():
    device = "cuda" \
        if torch.cuda.is_available() \
        else "mps" if torch.backends.mps.is_available() \
        else "cpu"
    if device == "mps":
        import os
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
    return torch.device(device)


class_names = [
    "greetings",
    "company", 
    "feedbacks", 
    "continue_later", 
    "stop_continue",
    "trouble",
    "himself",
    "continue_yes",
]

id2label = {i: label for i, label in enumerate(class_names)}


model_save_path = "/Users/beltre.wilton/apps/tars/samantha/src/roberta_base_ft"
tokenizer_save_path = "/Users/beltre.wilton/apps/tars/samantha/src/roberta_base_ft_tokenizer"

fine_tuned_model = RobertaForSequenceClassification.from_pretrained(model_save_path)
fine_tuned_tokenizer = RobertaTokenizerFast.from_pretrained(tokenizer_save_path)

print("⚡️ Model [fine_tuned_model] loaded.")


# Load the tokenizer and model
cefr_grammar_tokenizer = AutoTokenizer.from_pretrained("hafidikhsan/distilbert-base-uncased-english-cefr-lexical-evaluation-dt-v1")
cefr_grammar_model = AutoModelForSequenceClassification.from_pretrained("hafidikhsan/distilbert-base-uncased-english-cefr-lexical-evaluation-dt-v1")
print("⚡️ Model [distilbert-base-uncased-english-cefr] loaded.")


odoo_message = OdooMessages(get_odoo())
print('⚡️ Odoo RPC loaded')