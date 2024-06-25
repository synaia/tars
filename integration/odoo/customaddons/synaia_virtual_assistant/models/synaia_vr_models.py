from odoo import models, fields

class va_message_history(models.Model):
    _name = 'va.message.history'
    _description = 'History Message'

    msisdn = fields.Char(string='Phone Number', required=True)
    campaign = fields.Char(string='Campaign', required=True)
    human_message = fields.Char(string='Human Message')
    lm_message = fields.Text(string='LLM Message')

class va_stage(models.Model):
    _name = 'va.stage'
    _description = 'Stage'

    msisdn = fields.Char(string='Phone Number', required=True)
    campaign = fields.Char(string='Campaign', required=True)
    state = fields.Char(string='State')
    last_update = fields.Datetime(string='Last Update')

class va_task(models.Model):
    _name = 'va.task'
    _description = 'Task'

    msisdn = fields.Char(string='Phone Number', required=True)
    campaign = fields.Char(string='Campaign', required=True)
    task = fields.Char(string='Task')
    complete = fields.Boolean(string='Is Complete?')
    message_id = fields.Text(string='Message')
    last_update = fields.Datetime(string='Last Update')

class va_schedule(models.Model):
    _name = 'va.schedule'
    _description = 'Schedule'

    msisdn = fields.Char(string='Phone Number', required=True)
    campaign = fields.Char(string='Campaign', required=True)
    schedule = fields.Datetime(string='Schedule')

class va_applicant_recording(models.Model):
    _name = 'va.applicant.recording'
    _description = 'Applicant Recording'

    msisdn = fields.Char(string='Phone Number', required=True)
    campaign = fields.Char(string='Campaign', required=True)
    audio_path = fields.Char(string='Audio URL')