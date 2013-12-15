FROM localhost:5000/oracle-java7
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN useradd --comment zookeeper --user-group --uid 2181 --gid 2181 --no-create-home zookeeper
RUN install -d -o zookeeper -g zookeeper /var/lib/zookeeper~
ADD https://www.apache.org/dist/zookeeper/zookeeper-3.4.5/zookeeper-3.4.5.tar.gz /opt
ADD zoo.cfg /opt/zookeeper-3.4.5/conf/zoo.cfg

USER zookeeper
WORKDIR /opt/zookeeper-3.4.5
VOLUME /var/lib/zookeeper
CMD [ "./bin/zkServer.sh", "start-foreground" ]
