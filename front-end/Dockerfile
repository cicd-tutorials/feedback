FROM node:lts as build

WORKDIR /app
COPY ./package* /app/
RUN npm ci

COPY . /app
RUN npm run build


FROM nginx:alpine

ENV PROXY_PASS=""

COPY --from=build /app/dist /usr/share/nginx/html

RUN rm -f /etc/nginx/conf.d/*
COPY default.conf.template /etc/nginx/templates/
