FROM nginx:alpine

ENV PROXY_PASS=""

COPY index.html styles.css script.js config.js /usr/share/nginx/html/

RUN rm -f /etc/nginx/conf.d/*
COPY default.conf.template /etc/nginx/templates/
