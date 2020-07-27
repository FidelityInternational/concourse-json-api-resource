FROM python:3.8-alpine

RUN apk add --no-cache --update jq && \
    pip install --upgrade pip && \
    pip install --upgrade requests requests_mock dpath

ADD assets/ /opt/resource/