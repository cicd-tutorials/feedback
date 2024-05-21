FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt && pip install psycopg2-binary

COPY server.py /app/
ENTRYPOINT ["gunicorn", "--access-logfile", "-", "server:app"]
CMD ["-w", "4", "-b", "0.0.0.0:8000"]
