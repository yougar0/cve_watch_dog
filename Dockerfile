FROM ubuntu:20.04

WORKDIR /code

RUN mkdir /root/.pip

COPY pip.conf /root/.pip/

COPY sources.list /etc/apt/

RUN apt update && apt install python3 python3-pip vim -y

COPY monitor monitor

RUN pip3 install -r monitor/requirements.txt