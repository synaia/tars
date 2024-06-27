from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Applicant(models.Model):
    _inherit = 'hr.applicant'
    
    #Speech Overall score
    speech_overall_score = fields.Float(string='Speech Overall Score', default=0.0)    
    #Pronunciation Score
    speech_duration = fields.Float(string='Duration of speech', help="Long of the voice note of this applicant", default=0.0)
    speech_fluency = fields.Float(string='Fluency of speech', help="Fluency of this applicant", default=0.0)
    speech_integrity = fields.Float(string='Integrity of speech', help="Integrity of this applicant", default=0.0)
    speech_pronunciation = fields.Float(string='Pronunciation of speech', help="Pronunciation of this applicant", default=0.0)
    speech_rhythm = fields.Float(string='Rhythm of speech', help="Rhythm of this applicant", default=0.0)
    speech_speed = fields.Float(string='Speed of speech', help="Speed of this applicant", default=0.0)
    speech_warning = fields.Char(string='Warning', size=300)
