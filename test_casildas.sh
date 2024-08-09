curl -i -X POST \
  https://graph.facebook.com/v19.0/361199733748751/messages \
  -H 'Authorization: Bearer ' \
  -H 'Content-Type: application/json' \
  -d '{ "messaging_product": "whatsapp", "to": "18296456177", "type": "template", "template": { "name": "hello_world", "language": { "code": "en_US" } } }'