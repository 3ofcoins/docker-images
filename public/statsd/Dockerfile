# -*- conf -*-
FROM 3ofcoins/nodejs
#TAG 0.7.1
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

ADD https://github.com/etsy/statsd/archive/v0.7.1.tar.gz /opt/
RUN tar -C /opt -xzvf /opt/v0.7.1.tar.gz && rm /opt/v0.7.1.tar.gz
ADD config.js /opt/statsd-0.7.1/

EXPOSE  8125/udp
EXPOSE  8126/tcp

USER nobody
WORKDIR /opt/statsd-0.7.1
ENTRYPOINT [ "/usr/bin/node" ]
CMD [ "stats.js", "config.js" ]
