from odoo import models, fields, api

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    lead_stage = fields.Char(string="Lead Stage", compute="_compute_lead_stage")
    lead_heat_check = fields.Char(string="Lead Heat Check", compute="_compute_lead_heat_check")
    lead_max_temperature = fields.Float(string='Max Lead Temperature', default=100)
    lead_temperature = fields.Float(string="Lead Temperature", compute="_compute_lead_temperature")

    def _compute_lead_stage(self):
        for record in self:
            self.env.cr.execute("""
                SELECT h.lead_stage 
                FROM public.hr_applicant AS a
                INNER JOIN public.hr_heat_check AS h
                ON a.id = h.applicant_id
                WHERE a.id = %s
            """, (record.id,))
            result = self.env.cr.fetchone()
            record.lead_stage = result[0] if result else ''

    def _compute_lead_heat_check(self):
        for record in self:
            self.env.cr.execute("""
                SELECT h.lead_heat_check 
                FROM public.hr_applicant AS a
                INNER JOIN public.hr_heat_check AS h
                ON a.id = h.applicant_id
                WHERE a.id = %s
            """, (record.id,))
            result = self.env.cr.fetchone()
            record.lead_heat_check = result[0] if result else ''

    def _compute_lead_temperature(self):
        for record in self:
            self.env.cr.execute("""
                SELECT h.lead_temperature
                FROM public.hr_applicant AS a
                INNER JOIN public.hr_heat_check AS h
                ON a.id = h.applicant_id
                WHERE a.id = %s
            """, (record.id,))
            result = self.env.cr.fetchone()
            record.lead_temperature = result[0] if result else 0
