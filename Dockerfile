FROM node:lts as build

ARG VITE_BUILD
WORKDIR /app
COPY front-end/package* /app/
RUN npm ci

COPY front-end /app
RUN npm run build


FROM python:3.11-slim as static

ENV FEEDBACK_HOME=/var/feedback/
ENV STATIC_ROOT=/app/static/
WORKDIR /app
COPY back-end/requirements.txt /app/
RUN pip install -r requirements.txt && pip install psycopg2-binary

COPY back-end .
RUN python3 manage.py collectstatic --no-input;


FROM nginx:alpine

ENV PROXY_PASS=""

COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=static /app/static /app/static

RUN rm -f /etc/nginx/conf.d/*
COPY front-end/default.conf.template /etc/nginx/templates/
