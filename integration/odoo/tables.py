import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import JSON
from integration.odoo.schema import Stage, Task, Schedule, Applicant, GrammarScore, PronunciationScore
from samantha.src.configs import Base
from integration.odoo.util import get_odoo


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
    __tablename__ = "va_stage_app"
    id = Column(Integer, primary_key=True, index=True)
    msisdn = Column(String, index=True)
    campaign = Column(String, index=True)
    state = Column(String)
    last_update = Column(DateTime)

class HrApplicant(Base):
    __tablename__ = 'hr_applicant'

    id = Column(Integer, primary_key=True)
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
    create_uid = Column(Integer)
    write_uid = Column(Integer)
    phone_sanitized = Column(String)
    email_normalized = Column(String)
    email_cc = Column(String)
    name = Column(String, nullable=False)
    email_from = Column(String)
    priority = Column(String)
    salary_proposed_extra = Column(String)
    salary_expected_extra = Column(String)
    partner_name = Column(String)
    partner_phone = Column(String)
    partner_phone_sanitized = Column(String)
    partner_mobile = Column(String)
    partner_mobile_sanitized = Column(String)
    kanban_state = Column(String, nullable=False)
    linkedin_profile = Column(String)
    availability = Column(DateTime)
    applicant_properties = Column(JSON)
    description = Column(Text)
    active = Column(Boolean)
    create_date = Column(DateTime)
    date_closed = Column(DateTime)
    date_open = Column(DateTime)
    date_last_stage_update = Column(DateTime)
    write_date = Column(DateTime)
    probability = Column(Float)
    salary_proposed = Column(Float)
    salary_expected = Column(Float)
    delay_close = Column(Float)
    cefr_score = Column(String)
    pron_c_score = Column(String)
    flue_c_score = Column(String)
    voca_c_score = Column(String)
    gram_c_score = Column(String)
    pron_score = Column(Float)
    flue_score = Column(Float)
    voca_score = Column(Float)
    gram_score = Column(Float)
    a1_score = Column(Integer)
    a2_score = Column(Integer)
    b1_score = Column(Integer)
    b2_score = Column(Integer)
    c1_score = Column(Integer)
    c2_score = Column(Integer)
    lead_last_client_update = Column(DateTime)
    lead_last_update = Column(DateTime)

class RecruitmentStage(Base):
    __tablename__ = "hr_recruitment_stage"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(JSON)

class SpeechaceLog(Base):
    __tablename__ = 'speechace_log'

    id = Column(Integer, primary_key=True)
    msisdn = Column(String(50), nullable=False)
    campaign = Column(String(100), nullable=False)
    response = Column(JSON)
    audio_path = Column(String(300))
    response_date = Column(DateTime)

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
                'job_id': 3,
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