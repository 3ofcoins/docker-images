FROM localhost:5000/oracle-java7
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN apt-get update && apt-get install --yes libcurl3
RUN ln -s /usr/lib/jvm/java-7-oracle/jre/lib/*/server/libjvm.so /usr/lib/libjvm.so

ADD https://s3.amazonaws.com/downloads.mesosphere.io/master/ubuntu/12.04/mesos_0.14.2_amd64.deb /tmp/mesos_0.14.2_amd64.deb
RUN dpkg -i /tmp/mesos_0.14.2_amd64.deb && rm -v /tmp/mesos_0.14.2_amd64.deb

ADD start /start

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

USER nobody
CMD [ "/start" ]
