from psycopg2 import sql
from odoo import models, fields


def refresh_grants(clz: models.Model, table_name: str) -> None:
    """
    Refreshes the ownership and grants for a specific database table.
    Args:
        clz (models.Model): The model instance that owns the table.
        table_name (str): The name of the table to refresh grants for.
    Notes:
        This function alters the ownership of the table to 'drfadul' and grants all privileges to 'drfadul'.
    Raises:
        None (but prints an error message if an Exception occurs during execution)
    """
    table_name = table_name.replace(".", "_")
    query = f""" 
         ALTER TABLE public.{table_name} OWNER TO drfadul;
         GRANT ALL ON TABLE public.{table_name} TO drfadul;
        """
    try:
        clz.env.cr.execute(
            sql.SQL(query)
        )
    except Exception as ex:
        print("**** problems ", ex)


class va_chat_history(models.Model):
    _name = 'va.chat.history'
    _description = 'Chat History Message'

    msisdn = fields.Char(string='Whatsapp Phone Number', required=True, index=True)
    campaign = fields.Char(string='Campaign', required=True, index=True)
    message = fields.Text(string='Any Message')
    source = fields.Char(string="human/ai source", size=100)
    whatsapp_id = fields.Char(string="Whatsapp id from json webhook", size=100, index=True)
    sending_date = fields.Datetime(string="Scheduled sending date time")
    readed = fields.Boolean(string="To notify if the message was readed")
    collected = fields.Boolean(string="To collect or group separate meesages sended arbitrary by user")

    def init(self):
        refresh_grants(self, table_name=self._name)

class va_applicant_stage(models.Model):
    _name = 'va.applicant.stage'
    _description = 'Applicant Stage'

    msisdn = fields.Char(string='Phone Number', required=True, index=True)
    campaign = fields.Char(string='Campaign', required=True, index=True)
    state = fields.Char(string='State', size=20)
    last_update = fields.Datetime(string='Last Update')

    def init(self):
        refresh_grants(self, table_name=self._name)

class va_speech_log(models.Model):
    _name = 'va.speech.log'
    _description = 'Speech Log'

    msisdn = fields.Char(string='Phone Number', required=True, index=True)
    campaign = fields.Char(string='Campaign', required=True, index=True)
    response = fields.Json(string='Full Json Speech Response')
    audio_path = fields.Char(string='The user recording audio path', size=500)

    def init(self):
        refresh_grants(self, table_name=self._name)
