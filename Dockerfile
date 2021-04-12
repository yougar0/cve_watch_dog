FROM ubuntu:20.04

WORKDIR /code

RUN mkdir /root/.pip

COPY pip.conf /root/.pip/

COPY sources.list /etc/apt/

RUN apt update && apt install python3 python3-pip -y

RUN pip3 install pip --upgrade

COPY monitor monitor

RUN pip3 install -r monitor/requirements.txt