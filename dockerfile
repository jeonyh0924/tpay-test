FROM        python:3.8.2-slim
MAINTAINER  hungyb0924@gmail.com

ENV         LANG            C.UTF-8

RUN         apt -y update
RUN         apt -y dist-upgrade
RUN         apt -y install gcc nginx supervisor && \
            pip3 install uwsgi && \
            apt -y remove gcc && \
            apt -y autoremove

COPY        requirements.txt /tmp/
RUN         pip3 install -r /tmp/requirements.txt

COPY        ./ /srv/tpay/
WORKDIR     /srv/tpay

WORKDIR     /srv/tpay/app
RUN         python3 manage.py collectstatic --noinput

# Nginx
# 기존에 존재하던 Nginx 설정파일들 삭제
RUN         rm -rf  /etc/nginx/sites-available/* && \
            rm -rf  /etc/nginx/sites-enabled/* && \
            cp -f   /srv/tpay/.config/app.nginx \
                    /etc/nginx/sites-available/ && \
            ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

RUN         cp -f   /srv/tpay/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

# docker 로 컨테이너를 실행시키고 80번 포트 개방하면 요청 처리가 가능
EXPOSE      80

# Command로 supervisor실행
CMD         supervisord -n
