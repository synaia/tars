curl -i -X POST \
  https://graph.facebook.com/v19.0/340502765810581/messages \
  -H 'Authorization: Bearer ' \
  -H 'Content-Type: application/json' \
  -d '{ "messaging_product": "whatsapp", "to": "18296456177", "type": "template", "template": { "name": "welcome_message", "language": { "code": "en_US" } } }'