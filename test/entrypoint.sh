#!/bin/sh

echo "Waiting for the server to be ready..."
url="${BASE_URL:-http://localhost:8080}/api/question/thumbs"
until curl -sf $url; do
  sleep 3;
done

exec robot "$@" ./suites