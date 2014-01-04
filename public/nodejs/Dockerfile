# -*- conf -*-
FROM ubuntu:12.04
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install --yes python-software-properties
RUN add-apt-repository --yes ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install nodejs

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

ENTRYPOINT [ "/usr/bin/node" ]
