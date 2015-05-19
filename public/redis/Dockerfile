# -*- conf -*-

FROM ubuntu:14.04
#TAG 3.0.1
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 5862E31D
RUN echo 'deb http://ppa.launchpad.net/rwky/redis/ubuntu trusty main' > /etc/apt/sources.list.d/rwky-redis.list
RUN apt-get update --yes
RUN apt-get install --yes runit redis-server=2:3.0.1-rwky1~trusty

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
ADD redis.conf /etc/redis/redis.conf
ADD server /server
ADD cli /cli

EXPOSE 6379
VOLUME /var/lib/redis
CMD [ "/server" ]
