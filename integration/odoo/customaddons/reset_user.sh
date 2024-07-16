source .remote_secret

echo "DELERING ${1} ..."

redis-cli --scan --pattern "${1}:GET_FROM_SENDER" | xargs -L 1 redis-cli del;
redis-cli --scan --pattern "record:${1}:GET_FROM_SENDER:*" | xargs -L 1 redis-cli del;
redis-cli --scan --pattern "state:${1}:GET_FROM_SENDER" | xargs -L 1 redis-cli del;

sshpass -p "$elmer_pass" psql -v -d synaia --host=138.197.112.92 --port=5432 --username=drfadul -c "DELETE FROM va_chat_history WHERE msisdn = '${1}'"
sshpass -p "$elmer_pass" psql -v -d synaia --host=138.197.112.92 --port=5432 --username=drfadul -c "DELETE FROM va_applicant_stage WHERE msisdn = '${1}'"

