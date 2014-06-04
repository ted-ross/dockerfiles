FROM fedora:20
MAINTAINER Ted Ross <tross@apache.org>
RUN yum -y update
RUN yum -y install httpd python-qpid-proton git gcc cmake python-devel qpid-proton-c-devel
RUN sed -i -e 's/#ServerName www.example.com:80/ServerName 0.0.0.0:80/' /etc/httpd/conf/httpd.conf
RUN sed -i -e 's/# Redirect permanent \/foo http:\/\/www.example.com\/bar/Redirect permanent \/index.html \/cgi-bin\/qdweb.py/' /etc/httpd/conf/httpd.conf
RUN git clone git://git.apache.org/dispatch.git
RUN mkdir dispatch/build
RUN cd dispatch/build; cmake -DCMAKE_INSTALL_PREFIX=/usr ..; make install
ADD start.sh /start.sh
ADD index.png /var/www/html/index.png
RUN chmod +x /start.sh
ADD qdweb.css /var/www/html/css/qdweb.css
ADD qdweb.py /var/www/cgi-bin/qdweb.py
RUN chmod +x /var/www/cgi-bin/qdweb.py
CMD /start.sh

