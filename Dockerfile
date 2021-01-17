FROM ubuntu:18.04

# author
MAINTAINER Manveer Singh

# extra metadata
LABEL version="1.0"
LABEL description="PiExchange-Manveer"

# update sources list & install python 3.8
RUN apt-get clean && apt-get update && apt-get install -qy python3.8-minimal && apt-get install -qy python3-pip

COPY . /app
ENV PYTHONPATH /app/
WORKDIR /app

RUN pip3 install -r requirements.txt

