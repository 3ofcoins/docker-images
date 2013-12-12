# -*- conf -*-

FROM ubuntu:12.04
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

# Basic system preparation
RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install --yes python-software-properties lsb-release
RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu `lsb_release -sc` main universe multiverse"
RUN apt-get update --yes
RUN dpkg-divert --local --rename --add /sbin/initctl && ln -s /bin/true /sbin/initctl # needed to install some packages
RUN apt-get install --yes net-tools # `ip route` is used to find IP of the Docker host

# Prerequisites
RUN apt-get install --yes python2.7 python2.7-dev postgresql-client-9.1 libpq-dev ca-certificates runit

# Virtualenv
ADD https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz /tmp/
RUN python2.7 /tmp/virtualenv-1.10.1/virtualenv.py /opt/sentry && rm -rf /tmp/virtualenv-1.10.1

# Installation of Sentry
RUN /opt/sentry/bin/pip install 'sentry[postgresql]' psycopg2 python-memcached redis hiredis nydus
RUN useradd --comment sentry --user-group --no-create-home sentry

# Add this services directory
ADD settings.py /etc/sentry/settings.py
ADD sentry /sentry

# Cleanup
RUN dpkg -l | awk '$2 ~ /-dev$/ { print $2 }' | xargs apt-get purge --yes cpp gcc binutils manpages
RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

EXPOSE 9000
ENTRYPOINT [ "/sentry" ]
