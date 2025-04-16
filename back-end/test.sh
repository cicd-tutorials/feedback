#!/bin/sh -xe

base_url=${1:-localhost\:5000}

# Wait until server is online
for i in $(seq 1 60); do
    curl $base_url/feedback/thumbs && break || true
    sleep 1
done

check_summary() {
    len=$(curl -s $base_url/feedback/thumbs/answer | jq 'length')
    test "$len" -eq $1

    positive=$(curl -s $base_url/feedback/thumbs/summary | jq .'values."1"')
    test "$positive" -eq $2
    negative=$(curl -s $base_url/feedback/thumbs/summary | jq .'values."-1"')
    test "$negative" -eq $3
    empty=$(curl -s $base_url/feedback/thumbs/summary | jq .'values.""')
    test "$empty" -eq $4
}

len=$(curl -s $base_url/feedback/thumbs/answer | jq 'length')
test "$len" -eq 0

feedback="1
-1
1"

for i in $feedback; do
    curl -s -X POST -H "Content-Type: application/json" -d "{\"value\":$i, \"submit\": true}" $base_url/feedback/thumbs/answer
done;

last=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"value\": -1}" $base_url/feedback/thumbs/answer | jq .id -r)

check_summary 4 2 2 0

curl -s -X PATCH -H "Content-Type: application/json" -d "{\"value\": 1, \"submit\": true}" $base_url/feedback/thumbs/answer/$last
curl -s -X POST -H "Content-Type: application/json" -d "{}" $base_url/feedback/thumbs/answer

check_summary 5 3 1 1
