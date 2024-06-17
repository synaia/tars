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
    lm_message: str | None = None

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