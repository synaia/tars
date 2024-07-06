from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class Applicant(BaseModel):
    campaign_id: Optional[int] = None
    source_id: Optional[int] = None
    medium_id: Optional[int] = None
    message_bounce: Optional[int] = 0
    message_main_attachment_id: Optional[int] = None
    partner_id: Optional[int] = None
    stage_id: Optional[int] = 1
    last_stage_id: Optional[int] = None
    company_id: Optional[int] = 1
    user_id: Optional[int] = None
    job_id: Optional[int] = 1
    type_id: Optional[int] = None
    department_id: Optional[int] = None
    color: Optional[int] = 0
    emp_id: Optional[int] = None
    refuse_reason_id: Optional[int] = None
    create_uid: Optional[int] = 1
    write_uid: Optional[int] = 1
    phone_sanitized: Optional[str] = None
    email_normalized: Optional[str] = None
    email_cc: Optional[str] = None
    name: Optional[str] = None
    email_from: Optional[str] = None
    priority: Optional[str] = 0
    salary_proposed_extra: Optional[str] = None
    salary_expected_extra: Optional[str] = None
    partner_name: Optional[str] = None
    partner_phone: Optional[str] = None
    partner_phone_sanitized: Optional[str] = None
    partner_mobile: Optional[str] = None
    partner_mobile_sanitized: Optional[str] = None
    kanban_state: str = 'normal'
    linkedin_profile: Optional[str] = None
    availability: Optional[datetime] = None
    applicant_properties: Optional[Dict] = None
    description: Optional[str] = None
    active: Optional[bool] = True
    date_closed: Optional[datetime] = None
    date_open: Optional[datetime] = None
    date_last_stage_update: Optional[datetime] = None
    probability: Optional[float] = None
    salary_proposed: Optional[float] = None
    salary_expected: Optional[float] = None
    delay_close: Optional[float] = None
    speech_warning: Optional[str] = None
    a1_score: Optional[float] = None
    a2_score: Optional[float] = None
    b1_score: Optional[float] = None
    b2_score: Optional[float] = None
    c1_score: Optional[float] = None
    c2_score: Optional[float] = None
    user_input_text: Optional[str] = None
    lead_last_update: Optional[datetime] = None
    lead_last_client_update: Optional[datetime] = None
    lead_max_temperature: Optional[float] = None
    lead_heat_check: Optional[str] = None
    speech_open_question: Optional[str] = None
    speech_unscripted_overall_score: Optional[float] = None
    speech_unscripted_length: Optional[float] = None
    speech_unscripted_fluency_coherence: Optional[float] = None
    speech_unscripted_grammar: Optional[float] = None
    speech_unscripted_lexical_resource: Optional[float] = None
    speech_unscripted_pause_filler: Optional[Dict] = None
    speech_unscripted_pronunciation: Optional[float] = None
    speech_unscripted_relevance: Optional[float] = None
    speech_unscripted_speed: Optional[float] = None
    speech_unscripted_transcription: Optional[str] = None
    speech_unscripted_audio_path: Optional[str] = None
    speech_unscripted_warning: Optional[str] = None
    speech_overall: Optional[float] = None
    speech_refText: Optional[str] = None
    speech_duration: Optional[float] = None
    speech_fluency: Optional[float] = None
    speech_integrity: Optional[float] = None
    speech_pronunciation: Optional[float] = None
    speech_rhythm: Optional[float] = None
    speech_speed: Optional[str] = None
    speech_audio_path: Optional[str] = None
    speech_warning: Optional[str] = None
    create_date: Optional[datetime] = None
    write_date: Optional[datetime] = None

    class Config:
        orm_mode = True


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
    user_input_text: str | None = None

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
    speech_unscripted_pause_filler: dict | None = None
    speech_unscripted_pronunciation: float | None = None
    speech_unscripted_relevance: float | None = None
    speech_unscripted_speed: float | None = None
    speech_unscripted_audio_path: str | None = None
    speech_unscripted_transcription: str | None = None
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