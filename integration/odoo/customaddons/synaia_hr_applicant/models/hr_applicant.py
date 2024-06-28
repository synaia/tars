from psycopg2 import sql

from odoo import tools
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    lead_stage = fields.Char(string="Lead Stage", compute="_compute_lead_stage")
    lead_heat_check = fields.Char(string="Lead Heat Check", compute="_compute_lead_heat_check")
    lead_max_temperature = fields.Float(string='Max Lead Temperature', default=100)
    lead_temperature = fields.Float(string="Lead Temperature", compute="_compute_lead_temperature")


    lead_last_update = fields.Datetime(string='Lead last update')
    lead_last_client_update = fields.Datetime(string='Lead client update')


    photo_applicant = fields.Binary("Applicant Photo", attachment=True)

     #Grammar score
    a1_score = fields.Float(string='A1', help="A1 score of this applicant", default=0.000, digits=(6, 3))
    a2_score = fields.Float(string='A2', help="A2 score of this applicant", default=0.000, digits=(6, 3))
    b1_score = fields.Float(string='B1', help="B1 score of this applicant", default=0.000, digits=(6, 3))
    b2_score = fields.Float(string='B2', help="B2 score of this applicant", default=0.000, digits=(6, 3))
    c1_score = fields.Float(string='C1', help="C1 score of this applicant", default=0.000, digits=(6, 3))
    c2_score = fields.Float(string='C2', help="C2 score of this applicant", default=0.000, digits=(6, 3))
    user_input_text = fields.Text(string="User input text")


    #UNScripted Speech Overall score
    speech_unscripted_overall_score = fields.Float(string='Speech Overall Score', default=0.0)    
    #***UNScripted Score
    speech_open_question = fields.Char(string='Open question', size=400)
    speech_unscripted_length = fields.Float(string='Length of speech', help="Length of the voice note of this applicant", default=0.0)
    speech_unscripted_fluency_coherence = fields.Float(string='Fluency coherence', help="Fluency coherence of this applicant", default=0.0)
    speech_unscripted_grammar = fields.Float(string='Grammar score', help="Grammar score  of this applicant", default=0.0)
    speech_unscripted_lexical_resource = fields.Float(string='Lexical score', help="Lexical score of this applicant", default=0.0)
    speech_unscripted_pause_filler = fields.Json(string='Pause fillers')
    speech_unscripted_pronunciation = fields.Float(string='Pronunciation', help="Pronunciation of this applicant", default=0.0)
    speech_unscripted_relevance = fields.Float(string='Relevance', help="Relevance of this applicant", default=0.0)
    speech_unscripted_speed = fields.Float(string='Speed', help="Speed of this applicant", default=0.0)
    speech_unscripted_transcription = fields.Text(string="Transcription")
    speech_unscripted_warning = fields.Char(string='Warning', size=300)
    speech_unscripted_audio_path = fields.Char(string='Audio path', size=300)

    #Scripted Score
    speech_overall = fields.Float(string="Overall score", default=0.0)
    speech_refText = fields.Text(string="Text readed by applicant")
    speech_duration = fields.Float(string="Audio/voice note duration", default=0.0)
    speech_fluency = fields.Float(string="Fluency score", default=0.0)
    speech_integrity = fields.Float(string="Integrity score", default=0.0)
    speech_pronunciation = fields.Float(string="Pronunciation score", default=0.0)
    speech_rhythm = fields.Float(string="Rhythm score", default=0.0)
    speech_speed = fields.Float(string="Speed score", default=0.0)
    speech_warning = fields.Char(string='Warning', size=300)
    speech_audio_path = fields.Char(string='Audio path', size=300)




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


    def init(self):
        query = """ 
        CREATE OR REPLACE FUNCTION computed_heat_check(p_id integer, p_lead_last_update timestamp, p_lead_last_client_update timestamp)
        RETURNS varchar AS $$
        DECLARE
            head_check_str varchar;
            v_kanban_stage  varchar;
        BEGIN
            SELECT 
                s.name->>'en_US' INTO v_kanban_stage
            FROM hr_applicant a, hr_recruitment_stage s
            WHERE a.id = p_id
            AND a.stage_id = s.id;

            IF v_kanban_stage <> 'Evaluation' THEN
                IF (NOW() - p_lead_last_update) BETWEEN INTERVAL '4 days' AND INTERVAL '7 days' THEN
                    head_check_str := 'warm';
                ELSIF (NOW() - p_lead_last_update) >  INTERVAL '7 days' THEN
                    head_check_str := 'cold';
                ELSE
                    head_check_str := 'hot';
                END IF;
            ELSE
                IF (NOW() - p_lead_last_client_update) BETWEEN INTERVAL '4 days' AND INTERVAL '7 days' THEN
                    head_check_str := 'warm';
                ELSIF (NOW() - p_lead_last_client_update) >  INTERVAL '7 days' THEN
                    head_check_str := 'cold';
                ELSE
                    head_check_str := 'hot';
                END IF;
            END IF;

            RETURN head_check_str;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;


        CREATE OR REPLACE FUNCTION computed_lead_temperature(p_lead_last_update timestamp)
        RETURNS decimal AS $$
        BEGIN
            IF (10 - EXTRACT(DAY FROM (NOW() - p_lead_last_update))) < 0.0 THEN
                RETURN 0.0;
            ELSE
                RETURN (10 - EXTRACT(DAY FROM (NOW() - p_lead_last_update))) * 0.1;
            END IF;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
        

        CREATE OR REPLACE VIEW  hr_heat_check AS
            SELECT 
                a.id AS applicant_id, s.name->>'en_US' AS lead_stage,
                a.lead_last_update, a.lead_last_client_update,
                computed_heat_check(a.id, a.lead_last_update, a.lead_last_client_update) AS lead_heat_check,
                computed_lead_temperature(a.lead_last_update) AS lead_temperature,
                computed_lead_temperature(a.lead_last_client_update) AS lead_client_temperature
            FROM hr_applicant a, hr_recruitment_stage s
            WHERE a.stage_id = s.id;

         ALTER TABLE public.hr_heat_check OWNER TO drfadul;
         
         GRANT ALL ON TABLE public.hr_heat_check TO drfadul;
        """
        try:
            self.env.cr.execute(
                sql.SQL(query)
            )
        except Exception as ex:
            print("**** problems ", ex)
