from odoo import models, fields, api

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    lead_last_update = fields.Datetime(string='Lead last update')
    lead_last_client_update = fields.Datetime(string='Lead client update')