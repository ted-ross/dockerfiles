FROM tedross/qpid-proton:0.22.0
RUN dnf -y install gettext hostname iputils libwebsockets-devel

ADD qpid-dispatch-binary.tar.gz /
ADD console-binary.tar.gz /
COPY ./qdrouterd.conf.template /etc/qpid-dispatch/
COPY ./run_qdr.sh /usr/sbin/

EXPOSE 5671 5672 55672 8080
CMD ["/usr/sbin/run_qdr.sh"]
