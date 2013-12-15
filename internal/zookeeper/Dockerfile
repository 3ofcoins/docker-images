FROM localhost:5000/oracle-java7
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN groupadd --gid 2181 zookeeper
RUN useradd --comment zookeeper --uid 2181 --gid zookeeper --no-create-home zookeeper
RUN install -d -o zookeeper -g zookeeper /var/lib/zookeeper /var/lib/zookeeper~
ADD https://www.apache.org/dist/zookeeper/zookeeper-3.4.5/zookeeper-3.4.5.tar.gz /opt
ADD zoo.cfg /opt/zookeeper-3.4.5/conf/zoo.cfg
ADD start /start

WORKDIR /opt/zookeeper-3.4.5
VOLUME /var/lib/zookeeper
CMD [ "/start" ]
