from psycopg2 import sql

from odoo import tools
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Applicant(models.Model):
    _inherit = 'hr.applicant'
    
    lead_last_update = fields.Datetime(string='Lead last update')
    lead_last_client_update = fields.Datetime(string='Lead client update')

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