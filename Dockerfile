FROM python:3.5.6-alpine

LABEL maintainer="E-cell"

ENV PYTHONBUFFERED 1

RUN adduser -D delta
USER delta

# install psycopg2 dependencies
RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev build-base py-pip jpeg-dev zlib-dev

# Install pip packages
RUN pip install --upgrade pip \
  && pip install --upgrade setuptools \
  && pip install --upgrade pipenv
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /usr/delta/delta-backend
WORKDIR /usr/delta/delta-backend
COPY . .

ENTRYPOINT ["/usr/delta/delta-backend/entrypoint.sh"]