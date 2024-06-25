from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Applicant(models.Model):
    _inherit = 'hr.applicant'
    
    #CEFR Overall score
    cefr_score = fields.Char(string='CEFR Overall Score', size=5)
    
    #Pronunciation Score
    pron_score = fields.Float(string='Pronunciation Score ', help="Pronunciation score of this applicant", default=0.0)
    pron_c_score = fields.Char(string='Pronunciation', size=5)

    #Fluency Score
    flue_score = fields.Float(string='Fluency Score       ', help="Fluency score of this applicant", default=0.0)
    flue_c_score = fields.Char(string='Fluency', size=5)

    #Vocabulary Score
    voca_score = fields.Float(string='Vocabulary Score    ', help="Vocabulary score of this applicant", default=0.0)
    voca_c_score = fields.Char(string='Vocabulary', size=5)

    #Gramma Score
    gram_score = fields.Float(string='Grammar Score       ', help="Gramma score of this applicant", default=0.0)
    gram_c_score = fields.Char(string='Grammar', size=5)

    # @api.constrains('pron_score', 'flue_score', 'voca_score', 'gram_score')
    # def _check_scores(self):
    #     for record in self:
    #         if not (0 <= record.pron_score <= 1):
    #             raise ValidationError("Pronunciation Score must be between 0 and 1.")
    #         if not (0 <= record.flue_score <= 1):
    #             raise ValidationError("Fluency Score must be between 0 and 1.")
    #         if not (0 <= record.voca_score <= 1):
    #             raise ValidationError("Vocabulary Score must be between 0 and 1.")
    #         if not (0 <= record.gram_score <= 1):
    #             raise ValidationError("Gramma Score must be between 0 and 1.")