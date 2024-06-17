import os
os.system('clear')
from samantha.src.state_machine import Stage
from integration.odoo.va import get_odoo, OdooMessages
from integration.whatsapp.whatsapp_client import WhatsAppClient

odoo_message = OdooMessages(odoo=get_odoo())
wtsapp_client = WhatsAppClient(debug=True)

while True:
    user_input = input("⚡️ ")
    if user_input.lower() == "quit": break
    msisdn = "18296456177"
    campaign = "GET_FROM_SENDER"
    utterance = user_input
    stage = Stage(msisdn=msisdn, campaign=campaign, odoo_message=odoo_message, wtsapp_client=wtsapp_client)
    r = stage.entry(text=utterance)
    print(r)


