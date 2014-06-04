# -*- conf -*-

FROM ubuntu:12.04
#TAG 6.4.4
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

# Prerequisites
RUN apt-get update --yes
RUN apt-get install --yes python2.7 python2.7-dev postgresql-client-9.1 libpq-dev ca-certificates runit

# Virtualenv
ADD https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz /tmp/
RUN python2.7 /tmp/virtualenv-1.10.1/virtualenv.py /opt/sentry && rm -rf /tmp/virtualenv-1.10.1

# Installation of Sentry
RUN /opt/sentry/bin/pip install 'sentry[postgres]==6.4.4' hiredis nydus
RUN /opt/sentry/bin/pip freeze | tee /opt/sentry/requirements-freeze.txt
RUN useradd --comment sentry --user-group --create-home --home /var/opt/sentry sentry

# Add this services directory
ADD env_remote_user_middleware.py /opt/sentry/local/lib/python2.7/site-packages/
ADD settings.py /etc/sentry/settings.py
ADD sentry /sentry

# Cleanup
RUN dpkg -l | awk '$2 ~ /-dev$/ { print $2 }' | xargs apt-get purge --yes cpp gcc binutils manpages
RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

EXPOSE 9000
ENTRYPOINT [ "/sentry" ]
CMD [ "start", "--noupgrade" ]
