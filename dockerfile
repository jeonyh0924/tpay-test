FROM        python:3.8.2-slim
MAINTAINER  hungyb0924@gmail.com

ENV         LANG            C.UTF-8

RUN         apt -y update
RUN         apt -y dist-upgrade

RUN         apt -y install gcc nginx supervisor
RUN         pip3 install gunicorn

COPY        requirements.txt /tmp/
RUN         pip3 install -r /tmp/requirements.txt

COPY        ./   /srv/project
WORKDIR     /srv/project/app
RUN         python3 manage.py collectstatic --noinput

RUN         rm -rf  /etc/nginx/sites-available/*
RUN         rm -rf  /etc/nginx/sites-enabled/*

RUN         cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/
RUN         ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

ENV         DJANGO_SETTINGS_MODULE  config.settings

RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/
CMD         supervisord -n
