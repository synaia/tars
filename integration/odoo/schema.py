from pydantic import BaseModel

class Applicant(BaseModel):
    name: str | None = None
    email: str | None = None
    eLevel: str | None = None
    phone_sanitized: str | None = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    code: str | None = None

    class Config:
        from_attributes = True


class Recording(BaseModel):
    binary_file: str | None = None

    class Config:
        from_attributes = True


class MessageHistory(BaseModel):
    msisdn: str | None = None
    campaign: str | None = None
    human_message: str | None = None
    lm_message: str | None = None

    class Config:
        from_attributes = True

class Stage(BaseModel):
    msisdn: str | None = None
    campaign: str | None = None
    state: str | None = None
    last_update: str | None = None

    class Config:
        from_attributes = True

class Task(BaseModel):
    msisdn: str | None = None
    campaign: str | None = None
    task: str | None = None
    complete: bool | None = None
    message_id: int | None = None
    last_update: str | None = None

    class Config:
        from_attributes = True


class Schedule(BaseModel):
    msisdn: str | None = None
    campaign: str | None = None
    schedule: str | None = None

    class Config:
        from_attributes = True      


class GrammarScore(BaseModel):
    msisdn: str | None = None
    a1_score: float | None = None
    a2_score: float | None = None
    b1_score: float | None = None
    b2_score: float | None = None
    c1_score: float | None = None
    c2_score: float | None = None

    class Config:
        from_attributes = True        


class PronunciationScore(BaseModel):
    msisdn: str | None = None
    cefr_score: str | None = None
    pronun_c: str | None = None
    fluent_c: str | None = None
    vocab_c: str | None = None
    gramm_c: str | None = None
    pronun: float | None = None
    fluent: float | None = None
    vocab: float | None = None
    gramm: float | None = None

    class Config:
        from_attributes = True                