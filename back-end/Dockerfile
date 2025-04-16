FROM python:3.11-slim

ENV FEEDBACK_HOME=/var/feedback/
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt && pip install psycopg2-binary

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
