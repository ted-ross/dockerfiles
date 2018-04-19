FROM fedora:27
RUN dnf -y install cyrus-sasl-lib cyrus-sasl-plain libuuid openssl python && dnf -y update && dnf clean all
ADD qpid-proton-binary.tar.gz /
CMD ["bash"]
