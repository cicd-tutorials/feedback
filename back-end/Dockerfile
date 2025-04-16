FROM python:3.11-slim

ENV FEEDBACK_HOME=/var/photo_objects/
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt && pip install psycopg2-binary

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
