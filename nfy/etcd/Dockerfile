FROM busybox

ADD https://github.com/coreos/etcd/releases/download/v0.2.0/etcd-v0.2.0-Linux-x86_64.tar.gz /opt/
RUN cd /opt && \
    tar -xzf etcd-v0.2.0-Linux-x86_64.tar.gz && \
    rm etcd-v0.2.0-Linux-x86_64.tar.gz

VOLUME /var/lib/docker
WORKDIR /var/lib/docker

ADD etcd.sh /usr/sbin/etcd
RUN chmod 0755 /usr/sbin/etcd

ENTRYPOINT [ "/usr/sbin/etcd" ]
CMD [ "#" ]
EXPOSE 127.0.0.1:4001:4001

ENV ETCD_ADDR 127.0.0.1:4001
