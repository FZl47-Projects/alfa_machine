FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING 'utf8'
ENV DJANGO_SUPERUSER_PASSWORD admin

RUN apt update -y && apt install gcc -y # install gcc for uwsgi lib

ADD ./src /app/src
ADD ./requirements.txt /app/
ADD ./uwsgi.ini /app/
ADD ./run.sh /app/
RUN chmod 777 /app/run.sh

WORKDIR /app
RUN pip install -r requirements.txt uwsgi pymysql[rsa] --timeout 1000 --retries 1000

RUN mkdir logs
WORKDIR /app/logs
RUN touch server.log && touch app.pid

WORKDIR /app/src

CMD while ! python manage.py sqlflush > /dev/null ; do sleep 1; done && \
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    /bin/sh -c /app/run.sh
