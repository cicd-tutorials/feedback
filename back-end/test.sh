#!/bin/sh -xe

base_url=${1:-localhost\:5000}

# Wait until server is online
for i in $(seq 1 60); do
    curl $base_url/feedback/how-are-you-feeling && break || true
    sleep 1
done

len=$(curl -s $base_url/feedback/how-are-you-feeling/answer | jq 'length')
test "$len" -eq 0

feedback="1
-1
1"

for i in $feedback; do
    curl -s -X POST -H "Content-Type: application/json" -d "{\"value\":$i, \"submit\": true}" $base_url/feedback/how-are-you-feeling/answer
done;

len=$(curl -s $base_url/feedback/how-are-you-feeling/answer | jq 'length')
test "$len" -eq 3

positive=$(curl -s $base_url/feedback/how-are-you-feeling/summary | jq .values.positive)
test "$positive" -eq 2
negative=$(curl -s $base_url/feedback/how-are-you-feeling/summary | jq .values.negative)
test "$negative" -eq 1
