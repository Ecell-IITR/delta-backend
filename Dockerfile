FROM python:3.5.6-alpine

LABEL maintainer="E-cell"

ENV PYTHONBUFFERED 1

# create the app user
# RUN addgroup -S delta && adduser -S delta -G delta

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

# # chown all the files to the delta user
# RUN chown -R delta:delta $APP_HOME \
#   && chmod -R o+r $APP_HOME

CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py migrate; gunicorn delta.wsgi:application -b 0.0.0.0:8000"]