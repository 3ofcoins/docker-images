# -*- conf -*-

FROM ubuntu:12.04
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get install --yes build-essential python2.7-dev python-cairo
RUN useradd --system --home=/opt/graphite/storage graphite

ADD https://pypi.python.org/packages/source/s/setuptools/setuptools-2.0.2.tar.gz /usr/src/
ADD https://pypi.python.org/packages/source/p/pip/pip-1.5.tar.gz /usr/src/
ADD requirements.txt /

RUN cd /usr/src/setuptools-* && python2.7 setup.py install
RUN cd /usr/src/pip-* && python2.7 setup.py install
RUN pip install -r /requirements.txt

ADD carbon.conf /opt/graphite/conf/
ADD storage-schemas.conf /opt/graphite/conf/
ADD storage-aggregation.conf /opt/graphite/conf/

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/pip* /usr/src/*

VOLUME /opt/graphite/storage
EXPOSE 2003
EXPOSE 2003/udp
EXPOSE 2004
