# -*- conf -*-

FROM ubuntu:12.04
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN apt-get update --yes
RUN apt-get install --yes openssl zlib1g libsqlite3-0 bzip2 ca-certificates

ADD https://downloads.egenix.com/python/egenix-pyrun-1.3.1-py2.7_ucs2-linux-x86_64.tgz /opt/pyrun/
ADD https://pypi.python.org/packages/source/s/setuptools/setuptools-2.0.2.tar.gz /tmp/
ADD https://pypi.python.org/packages/source/p/pip/pip-1.5.tar.gz /tmp/

RUN cd /tmp/setuptools-* && /opt/pyrun/bin/python setup.py install
RUN cd /tmp/pip-* && /opt/pyrun/bin/python setup.py install
RUN rm -rf /tmp/setuptools-* /tmp/pip-*
RUN ln -sfv /opt/pyrun/bin/* /usr/local/bin/

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
