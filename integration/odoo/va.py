import json
from datetime import datetime, timezone
import odoorpc
from .util import get_odoo
from .schema import Stage, Task, Schedule, Applicant

class OdooMessages():
    initial_state = "draft"

    def __init__(self, odoo: odoorpc.ODOO) -> None:
        self.odoo = odoo

    def create_messages(self, msisdn: str, campaign: str,  messages: list[str], chat_len: int) -> int:
        message = self.odoo.env['va.message.history']
        for msg in messages[chat_len:]:
            r = {
                'msisdn': msisdn,
                'campaign': campaign,
                'human_message': msg,
            }
            message.create(r)

        # self._update_applicant(msisdn, campaign)

    
    def get_messages(self, msisdn: str, campaign: str) -> list[str]:
        message_list = []
        message = self.odoo.env['va.message.history']
        ids = message.search([
                ('msisdn', '=', msisdn), ('campaign', '=', campaign)
            ], order="write_date asc"
        )
        for m in message.browse(ids):
            message_list.append(m.human_message)
        
        return message_list
    
    def update_stage(self, st: Stage) -> int:
        if isinstance(st, dict): st = Stage(**st)
        stage = self.odoo.env['va.stage']
        ids = stage.search([
            ('msisdn', '=', st.msisdn), ('campaign', '=', st.campaign)
        ])
        if len(ids) == 0:
            ids = stage.create({
                'msisdn': st.msisdn,
                'campaign': st.campaign,
                'state': st.state,
                'last_update': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            })
        else:
            state_record = stage.browse(ids)[0]
            state_record.state = st.state
            state_record.last_update = datetime.now(timezone.utc)
        
            # self._update_applicant(st.msisdn, st.campaign)

        return ids
    
    def get_stage(self, msisdn: str, campaign: str) -> str:
        stage = self.odoo.env['va.stage']
        ids = stage.search([
            ('msisdn', '=', msisdn), ('campaign', '=', campaign)
        ])
        if len(ids) > 0:
            state_record = stage.browse(ids)[0]
            return state_record.state
        else:
            self.update_stage({
                'msisdn': msisdn,
                'campaign': campaign,
                'state': OdooMessages.initial_state,
            })
            return OdooMessages.initial_state
    
    def _update_applicant(self, msisdn: str, campaign: str) -> int:
        appl = self.odoo.env['hr.applicant']
        ids = appl.search([
            ('phone_sanitized', '=', msisdn)
            #TODO: also filter by campaign
        ])
        appl_record = appl.browse(ids)[0]
        appl_record.lead_last_update = datetime.now(timezone.utc)

    def create_task(self, t: Task) -> int:
        if isinstance(t, dict): t = Task(**t)
        t.last_update = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        task = self.odoo.env['va.task']
        task_id = task.create({
            'msisdn': t.msisdn,
            'campaign': t.campaign,
            'task': t.task,
            'complete': False,
            'message_id': t.message_id,
            'last_update': t.last_update,
        })

        return task_id
    
    def close_task(self, t: Task) -> None:
        if isinstance(t, dict): t = Task(**t)
        task = self.odoo.env['va.task']
        ids = task.search([
                ('msisdn', '=', t.msisdn), ('campaign', '=', t.campaign), ('complete', '=', False),
            ],
            order="last_update desc"
        )
        if len(ids) > 0:
            task_record = task.browse(ids)[0]
            task_record.complete = True
            task_record.last_update = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    def get_task(self, t: Task) -> Task:
        if isinstance(t, dict): t = Task(**t)
        task = self.odoo.env['va.task']
        ids = task.search([
                ('msisdn', '=', t.msisdn), ('campaign', '=', t.campaign), ('complete', '=', False),
            ],
            order="last_update desc"
        )
        task_record = task.browse(ids)[0]
        return task_record

    def create_schedule(self, s: Schedule) -> int:
        schedule = self.odoo.env['va.schedule']
        s_id = schedule.create({
            'msisdn': s.msisdn,
            'campaign': s.campaign,
            'schedule': s.schedule,
        })
        return s_id

    def get_applicant_state(self, msisdn: str) -> str:
        print('Visiting odoo helper class ....')
        appl = self.odoo.env['hr.applicant']
        ids = appl.search([('phone_sanitized', '=', msisdn)]) #TODO: also filter by campaign
        state = appl.browse(ids)[0].stage_id.name
        return state
    
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

    def applicant_stage(self, state: str, msisdn: str):
        """
        1 - New (new -> basic form completed)
        2 - Grammar Check ()
        3 - QA Assestment (recording -> assesmetn have completed)
        7 - Recording (recording voice note received)
        4 - Evaluation (evaluation)
        """
        states = {
            'new': 1,
            'recording': 3,
            'evaluation': 4,
        }
        appl = self.odoo.env['hr.applicant']
        ids = appl.search([
            ('phone_sanitized', '=', msisdn)
            #TODO: also filter by campaign
        ])
        appl_record = appl.browse(ids)[0]
        appl_record.stage_id = states[state]
        

if __name__ == "__main__":
    odoo = get_odoo()
    m = OdooMessages(odoo=odoo)
    task_id =m.create_task({
        'msisdn': "18095673000",
        'campaign': "STODGO",
        'task': "question_2",
        'complete': False,
        'message_id': 1,
        'last_update': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
    })
    print(task_id)