from psycopg2 import sql
import logging
from odoo import tools
from odoo.tools.query import Query
from odoo.tools.sql import SQL
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class HrApplicant(models.Model):
    _inherit = 'hr.applicant' 

    heat_check_id = fields.One2many('hr.heat.check', 'applicant_id', string='Heat Check ID')

    lead_heat_check = fields.Char(related='heat_check_id.lead_heat_check', readonly=True,)
    lead_max_temperature = fields.Float(string='Max Lead Temperature', default=100)
    lead_temperature = fields.Float(related='heat_check_id.lead_temperature', readonly=True)
    lead_last_update = fields.Datetime(related='heat_check_id.lead_last_update', readonly=True)
    lead_last_client_update = fields.Datetime(related='heat_check_id.lead_last_client_update', readonly=True)

    dummy_date = fields.Datetime(related='heat_check_id.dummy_date', readonly=True, store=True, compute="_dummy_locura", ) # precompute=True


    photo_applicant = fields.Binary("Applicant Photo", attachment=True)

     #Grammar score
    a1_score = fields.Float(string='A1', help="A1 score of this applicant", default=0.000, digits=(6, 3))
    a2_score = fields.Float(string='A2', help="A2 score of this applicant", default=0.000, digits=(6, 3))
    b1_score = fields.Float(string='B1', help="B1 score of this applicant", default=0.000, digits=(6, 3))
    b2_score = fields.Float(string='B2', help="B2 score of this applicant", default=0.000, digits=(6, 3))
    c1_score = fields.Float(string='C1', help="C1 score of this applicant", default=0.000, digits=(6, 3))
    c2_score = fields.Float(string='C2', help="C2 score of this applicant", default=0.000, digits=(6, 3))
    cefr_score = fields.Char(string="Grammar Score", compute="_compute_cefr_score")
    grammar_score = fields.Float(string='G S', help="", default=0.000, digits=(6, 3))
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
    speech_unscripted_audio_path = fields.Char(string='Audio', size=300)

    ielts_max_value = fields.Float(string='ielts_max_value', default=9)

    #Scripted Score
    speech_overall = fields.Float(string="Scripted Score", default=0.0)
    speech_refText = fields.Text(string="Text readed by applicant")
    speech_duration = fields.Float(string="Audio/voice note duration", default=0.0)
    speech_fluency = fields.Float(string="Fluency", default=0.0)
    speech_integrity = fields.Float(string="Integrity", default=0.0)
    speech_pronunciation = fields.Float(string="Pronunciation", default=0.0)
    speech_rhythm = fields.Float(string="Rhythm", default=0.0)
    speech_speed = fields.Float(string="Speed", default=0.0)
    speech_warning = fields.Char(string='Warning', size=300)
    speech_audio_path = fields.Char(string='Audio', size=300)


    # def _compute_field_value(self, field):
    #     _logger.info(f" ----------------------------------> {field} -----")
    #     self._dummy_locura()
    #     return super()._compute_field_value(field)


    # def _field_to_sql(self, alias: str, fname: str, query: (Query | None) = None) -> SQL:
    #     """ Return an :class:`SQL` object that represents the value of the given
    #     field from the given table alias, in the context of the given query.
    #     The query object is necessary for inherited fields, many2one fields and
    #     properties fields, where joins are added to the query.
    #     """
    #     full_fname = fname
    #     property_name = None
    #     if '.' in fname:
    #         fname, property_name = fname.split('.', 1)

    #     field = self._fields[fname]
    #     if field.inherited:
    #         # retrieve the parent model where field is inherited from
    #         parent_model = self.env[field.related_field.model_name]
    #         parent_fname = field.related.split('.')[0]
    #         # LEFT JOIN parent_model._table AS parent_alias ON alias.parent_fname = parent_alias.id
    #         parent_alias = query.make_alias(alias, parent_fname)
    #         query.add_join('LEFT JOIN', parent_alias, parent_model._table, SQL(
    #             "%s = %s",
    #             self._field_to_sql(alias, parent_fname, query),
    #             SQL.identifier(parent_alias, 'id'),
    #         ))
    #         # delegate to the parent model
    #         return parent_model._field_to_sql(parent_alias, full_fname, query)
        
    #     if not full_fname == "lead_heat_check":
    #         if not field.store:
    #             raise ValueError(f"Cannot convert field {field} to SQL")
    #     else:
    #         _logger.info(f"|---------------------- {full_fname} -----------------------|")

    #     if field.type == 'many2many':
    #         # special case for many2many fields: prepare a query on the comodel
    #         # in order to reuse the mechanism _apply_ir_rules, then inject the
    #         # query as an extra condition of the left join
    #         comodel = self.env[field.comodel_name]
    #         coquery = comodel._where_calc([], active_test=False)
    #         comodel._apply_ir_rules(coquery)
    #         # LEFT JOIN {field.relation} AS rel_alias ON
    #         #     alias.id = rel_alias.{field.column1}
    #         #     AND rel_alias.{field.column2} IN ({coquery})
    #         rel_alias = query.make_alias(alias, field.name)
    #         condition = SQL(
    #             "%s = %s",
    #             SQL.identifier(alias, 'id'),
    #             SQL.identifier(rel_alias, field.column1),
    #         )
    #         if coquery.where_clause:
    #             condition = SQL(
    #                 "%s AND %s IN %s",
    #                 condition,
    #                 SQL.identifier(rel_alias, field.column2),
    #                 coquery.subselect(),
    #             )
    #         query.add_join("LEFT JOIN", rel_alias, field.relation, condition)
    #         return SQL.identifier(rel_alias, field.column2)

    #     elif field.translate and not self.env.context.get('prefetch_langs'):
    #         sql_field = SQL.identifier(alias, fname)
    #         langs = field.get_translation_fallback_langs(self.env)
    #         sql_field_langs = [SQL("%s->>%s", sql_field, lang) for lang in langs]
    #         if len(sql_field_langs) == 1:
    #             return sql_field_langs[0]
    #         return SQL("COALESCE(%s)", SQL(", ").join(sql_field_langs))

    #     elif field.type == 'properties' and property_name:
    #         return self._field_properties_to_sql(alias, fname, property_name, query)

    #     return SQL.identifier(alias, fname)


    def _dummy_locura(self):
       for record in self:
            self.env.cr.execute("""
                UPDATE hr_applicant a
                 SET dummy_date = (SELECT dummy_date FROM hr_heat_check h WHERE h.applicant_id = %s)
                WHERE a.id = %s
            """, (record.id, record.id,))
            _logger.info(f"********** {record.id}")


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

    @api.depends('lead_last_update')
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
            record.lead_heat_check = result[0] 
            # if result[0]:
            #     if result[0] == "hot":
            #         r = "hot 🔥"
            #     if result[0] == "warm":
            #         r = "warm 😎"
            #     if result[0] == "cold":
            #         r = "cold 🥶"
            #     record.lead_heat_check = r
            # else:
            #     record.lead_heat_check = ''

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

    def _compute_cefr_score(self):
        for record in self:
            scores = [
                {"A1": record.a1_score}, 
                {"A2": record.a2_score},
                {"B1": record.b1_score},
                {"B2": record.b2_score},
                {"C1": record.c1_score},
                {"C2": record.c2_score}
            ]
            try:
                max_score_dict = max(scores, key=lambda x: list(x.values())[0])
                print(scores)
            except Exception as ex:
                print(ex)
            max_score_string = list(max_score_dict.keys())[0]
            grammar_score_ = list(max_score_dict.values())[0]
            record.cefr_score = max_score_string
            record.grammar_score = grammar_score_



class HrHeatCheck(models.Model):
    _name = "hr.heat.check"
    _auto = False

    applicant_id = fields.Many2one('hr.applicant', string='Applicant ID')

    lead_stage = fields.Text(string="Lead stage")
    lead_last_update = fields.Datetime(string='Lead last update')
    lead_last_client_update = fields.Datetime(string='Lead client update')
    lead_heat_check = fields.Char(string='Lead Heat Check', size=10)
    lead_temperature = fields.Float(string='Lead Temperature')
    lead_client_temperature =fields.Float(string='lead_client_temperature')
    dummy_date  = fields.Datetime(string='Dummy date')

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
                row_number() OVER () AS id,
                a.id AS applicant_id, s.name->>'en_US' AS lead_stage,
                a.lead_last_update, a.lead_last_client_update,
                computed_heat_check(a.id, a.lead_last_update, a.lead_last_client_update) AS lead_heat_check,
                computed_lead_temperature(a.lead_last_update) AS lead_temperature,
                computed_lead_temperature(a.lead_last_client_update) AS lead_client_temperature,
                NOW()::timestamp AS dummy_date
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
