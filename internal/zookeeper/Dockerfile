FROM localhost:5000/oracle-java7
MAINTAINER Maciej Pasternacki <maciej@3ofcoins.net>

RUN useradd --comment zookeeper --user-group --no-create-home zookeeper
RUN install -d -o zookeeper -g zookeeper /data
ADD https://www.apache.org/dist/zookeeper/zookeeper-3.4.5/zookeeper-3.4.5.tar.gz /tmp/zookeeper.tar.gz
RUN tar -C /opt -xzvf /tmp/zookeeper.tar.gz && mv -v /opt/zookeeper-* /opt/zookeeper && rm /tmp/zookeeper.tar.gz
ADD zoo.cfg /opt/zookeeper/conf/zoo.cfg

USER zookeeper
WORKDIR /opt/zookeeper
VOLUME /var/lib/zookeeper
CMD [ "./bin/zkServer.sh" ]
