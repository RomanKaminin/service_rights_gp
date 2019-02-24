FROM python:3.6-slim


RUN apt-get update

WORKDIR /root/src/
ADD requirements.txt /root/src
RUN pip3 install -U pip
RUN pip3 install -Ur requirements.txt
ADD . /root/src/

EXPOSE 8080

