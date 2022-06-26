FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential
RUN apt-get install -y gcc
RUN apt-get update && apt-get install -y uwsgi
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get update && apt-get install libssl-dev
RUN apt-get install -y mariadb-client
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]