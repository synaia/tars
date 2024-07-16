import redis
import time
import argparse

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('number', type=str, help="phone number")
args = parser.parse_args()

pattern = f'record:{args.number}:GET_FROM_SENDER:*'
print(pattern)
keys_seen = set()

while True:
    # Scan for matching keys
    keys = list(r.scan_iter(match=pattern))
    new_keys = [key for key in keys if key not in keys_seen]

    if new_keys:
        records = []
        for key in new_keys:
            key_str = key.decode('utf-8')  # Assuming keys are byte strings
            # Fetch the hash fields
            record = r.hgetall(key_str)
            message = record.get(b'message', b'').decode('utf-8')
            source = record.get(b'source', b'').decode('utf-8')
            sending_date = record.get(b'sending_date', b'').decode('utf-8')
            records.append((key_str, message, source, sending_date))
            keys_seen.add(key)

        # Sort records by sending_date in descending order
        records.sort(key=lambda x: x[3], reverse=False)

        for record in records:
            print(f"{record[2]}: {record[1]}")
            print("\n")

    time.sleep(1)

