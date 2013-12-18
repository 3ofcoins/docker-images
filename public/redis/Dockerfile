# -*- conf -*-

FROM ubuntu:12.04
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN dpkg-divert --local --rename --add /sbin/initctl && ln -s /bin/true /sbin/initctl # needed to install some packages
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 5862E31D
RUN echo 'deb http://ppa.launchpad.net/rwky/redis/ubuntu precise main' > /etc/apt/sources.list.d/rwky-redis.list
RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install --yes redis-server

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
ADD redis.conf /etc/redis/redis.conf
ADD server /server
ADD cli /cli

EXPOSE 6379
VOLUME /var/lib/redis
CMD [ "/server" ]
