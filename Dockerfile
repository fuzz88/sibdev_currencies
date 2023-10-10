# ref: https://raw.githubusercontent.com/tough-dev-school/education-backend/master/Dockerfile

FROM python:3.11-slim-bullseye as base

LABEL maintainer="ivan@oschepkov.ru"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV CELERY_APP=app.celery

ENV _UWSGI_VERSION 2.0.21
ENV _WAITFOR_VERSION 2.2.3

RUN echo deb http://deb.debian.org/debian buster contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
  && apt-get update \
  && apt-get --no-install-recommends install -y wget tzdata netcat \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get --no-install-recommends install -y build-essential \
  && rm -rf /var/lib/apt/lists/*

# okay, mb will use later
RUN wget -O /usr/local/bin/wait-for https://github.com/eficode/wait-for/releases/download/v${_WAITFOR_VERSION}/wait-for \
  && chmod +x /usr/local/bin/wait-for

RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
  && tar zxvf uwsgi-*.tar.gz \
  && UWSGI_BIN_NAME=/usr/local/bin/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
  && rm -Rf uwsgi-*

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get remove -y build-essential
RUN apt-get autoremove -y


WORKDIR /src
COPY src /src

ENV NO_CACHE=On
RUN ./manage.py collectstatic --noinput
ENV NO_CACHE=Off
USER nobody


FROM base as web-with-static
HEALTHCHECK CMD wget -q -O /dev/null http://localhost:8888/healthchecks/status/ || exit 1
CMD ./manage.py migrate && ./manage.py runserver 0.0.0.0:8888

FROM base as web
HEALTHCHECK CMD wget -q -O /dev/null http://localhost:8888/healthchecks/status/ || exit 1
CMD ./manage.py migrate && uwsgi --master --http :8888 --module app.wsgi --workers 2 --threads 2 --harakiri 25 --max-requests 1000 --log-x-forwarded-for

FROM base as worker
HEALTHCHECK CMD celery -A ${CELERY_APP} inspect ping
CMD celery -A ${CELERY_APP} worker -E -c ${CONCURENCY:-2} --max-tasks-per-child ${MAX_REQUESTS_PER_CHILD:-50} --time-limit ${TIME_LIMIT:-900} --soft-time-limit ${SOFT_TIME_LIMIT:-45}

FROM base as flower
CMD celery -A ${CELERY_APP} flower

FROM base as scheduler
ENV SCHEDULER_DB_PATH=/var/db/scheduler
USER root
RUN mkdir -p ${SCHEDULER_DB_PATH} && chown nobody ${SCHEDULER_DB_PATH}
VOLUME ${SCHEDULER_DB_PATH}
USER nobody
HEALTHCHECK NONE
CMD celery -A ${CELERY_APP} beat --pidfile=/tmp/celerybeat.pid --schedule=${SCHEDULER_DB_PATH}/celerybeat-schedule.db