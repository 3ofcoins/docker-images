# -*- conf -*-

FROM ubuntu:12.04
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv C3173AA6
RUN echo 'deb http://ppa.launchpad.net/brightbox/ruby-ng/ubuntu precise main' > /etc/apt/sources.list.d/brightbox-ruby-ng.list
ADD apt_preferences /etc/apt/preferences.d/brightbox-ruby-ng

RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install ruby1.9.3 ruby1.9.1-full
RUN /usr/bin/gem install bundler

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
CMD [ "/usr/bin/irb" ]
