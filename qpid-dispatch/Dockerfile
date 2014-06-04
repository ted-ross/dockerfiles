##
## Licensed to the Apache Software Foundation (ASF) under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  The ASF licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing,
## software distributed under the License is distributed on an
## "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
## KIND, either express or implied.  See the License for the
## specific language governing permissions and limitations
## under the License.
##

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
ADD feather.png /var/www/html/feather.png
RUN chmod +x /start.sh
ADD qdweb.css /var/www/html/css/qdweb.css
ADD qdweb.py /var/www/cgi-bin/qdweb.py
RUN chmod +x /var/www/cgi-bin/qdweb.py
CMD /start.sh

