# -*- conf -*-
FROM 3ofcoins/nodejs
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

ADD https://github.com/etsy/statsd/archive/v0.7.0.tar.gz /opt/
ADD config.js /opt/statsd-0.7.0/

EXPOSE  8125/udp
EXPOSE  8126/tcp

USER nobody
WORKDIR /opt/statsd-0.7.0
ENTRYPOINT [ "/usr/bin/node" ]
CMD [ "stats.js", "config.js" ]
