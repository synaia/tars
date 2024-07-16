#!/bin/bash

# Define the pattern to match keys
pattern="record:18496576757:GET_FROM_SENDER:*"

# Scan for keys matching the pattern, sort them in reverse order, and process each key
redis-cli --scan --pattern "$pattern" | sort -r | while read key; do
  # Fetch the fields 'message' and 'source' from the hash
  message=$(redis-cli hget "$key" message)
  source=$(redis-cli hget "$key" source)
  # Print the key and its fields
  echo "Key: $key, Message: $message, Source: $source"
done

