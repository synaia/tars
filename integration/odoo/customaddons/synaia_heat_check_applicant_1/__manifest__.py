{
    'name': 'HR Applicant - Lead Temperature',
    'version': '17.0.1.0',
    'summary': 'Human Resources',
    'sequence': 10,
    'depends': ['hr_recruitment'],
    'data': [
        'views/hr_applicant_views.xml',
    ],
    'category': 'Human Resources',
    'author': 'Elmer Rodríguez - SYNAIA',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description': """
        Important: This module requires the creation of fields and running a database script.

        before install run this at db level:
        CREATE OR REPLACE VIEW public.hr_heat_check
        AS
            SELECT a.id AS applicant_id,
             s.name ->> 'en_US'::text AS lead_stage,
             a.lead_last_update,
             a.lead_last_client_update,
             computed_heat_check(a.id, a.lead_last_update, a.lead_last_client_update) AS lead_heat_check,
             computed_lead_temperature(a.lead_last_update) AS lead_temperature,
             computed_lead_temperature(a.lead_last_client_update) AS lead_client_temperature
            FROM hr_applicant a, hr_recruitment_stage s
           WHERE a.stage_id = s.id;
         
         ALTER TABLE public.hr_heat_check
             OWNER TO drfadul;
         
         GRANT ALL ON TABLE public.hr_heat_check TO drfadul;

    """,
}
