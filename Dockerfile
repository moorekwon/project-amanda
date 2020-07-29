FROM        python:3.7-slim

RUN         apt-get -y -qq update && \
            apt-get -y -qq dist-upgrade && \
            apt-get -u -qq autoremove

RUN         apt -y install nginx

# requirements.txt 복사
COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

# 소스 코드 복사
COPY        . /srv/project-amanda
WORKDIR     /srv/project-amanda/app

# nginx 기본 설정 삭제
RUN         rm /etc/nginx/sites-enabled/default
RUN         cp /srv/project-amanda/.config/prod/amanda.nginx /etc/nginx/sites-enabled/
RUN         mkdir /var/log/gunicorn

CMD         /bin/bash
