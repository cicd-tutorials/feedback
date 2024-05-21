#!/bin/sh -xe

base_url=${1:-localhost\:5000}

# Wait until server is online
for i in $(seq 1 60); do
    curl $base_url/feedback && break || true
    sleep 1
done

len=$(curl -s $base_url/feedback | jq 'length')
test "$len" -eq 0

feedback="positive
negative
positive"

for i in $feedback; do
    curl -s -X POST -H "Content-Type: application/json" -d "{\"type\":\"$i\"}" $base_url/feedback
done;

len=$(curl -s $base_url/feedback | jq 'length')
test "$len" -eq 3

positive=$(curl -s $base_url/feedback/summary | jq .positive)
test "$positive" -eq 2
negative=$(curl -s $base_url/feedback/summary | jq .negative)
test "$negative" -eq 1
