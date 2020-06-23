FROM python:3.5.6-alpine

LABEL maintainer="E-cell"

ENV PYTHONBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /usr/delta/delta-backend
WORKDIR /usr/delta/delta-backend
COPY . .

RUN adduser -D user
USER user