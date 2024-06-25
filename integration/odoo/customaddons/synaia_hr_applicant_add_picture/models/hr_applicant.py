from odoo import models, fields

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    photo_applicant = fields.Binary("Applicant Photo", attachment=True)