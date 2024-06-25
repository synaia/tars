from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Applicant(models.Model):
    _inherit = 'hr.applicant'
    
    #Grammar score
    a1_score = fields.Float(string='A1', help="A1 score of this applicant", default=0.000, digits=(6, 3))
    a2_score = fields.Float(string='A2', help="A2 score of this applicant", default=0.000, digits=(6, 3))
    b1_score = fields.Float(string='B1', help="B1 score of this applicant", default=0.000, digits=(6, 3))
    b2_score = fields.Float(string='B2', help="B2 score of this applicant", default=0.000, digits=(6, 3))
    c1_score = fields.Float(string='C1', help="C1 score of this applicant", default=0.000, digits=(6, 3))
    c2_score = fields.Float(string='C2', help="C2 score of this applicant", default=0.000, digits=(6, 3))