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


#TODO cambia todo
class SpeechScore(BaseModel):
    msisdn: str | None = None
    # 
    speech_open_question: str | None = None
    speech_unscripted_overall_score: float | None = None
    speech_unscripted_length: float | None = None
    speech_unscripted_fluency_coherence: float | None = None
    speech_unscripted_grammar: float | None = None
    speech_unscripted_lexical_resource: float | None = None
    speech_unscripted_pause_filler: str | None = None
    speech_unscripted_pronunciation: float | None = None
    speech_unscripted_relevance: float | None = None
    speech_unscripted_speed: float | None = None
    speech_unscripted_audio_path: str | None = None
    speech_unscripted_warning: str | None = None
    #
    speech_overall: float | None = None
    speech_refText: str | None = None
    speech_duration: float | None = None
    speech_fluency: float | None = None
    speech_integrity: float | None = None
    speech_pronunciation: float | None = None
    speech_rhythm: float | None = None
    speech_speed: float | None = None
    speech_audio_path: str | None = None
    speech_warning: str | None = None

    class Config:
        from_attributes = True                