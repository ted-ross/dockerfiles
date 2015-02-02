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

FROM fedora:21
MAINTAINER Ted Ross <tross@apache.org>
RUN yum -y update
RUN yum -y install cmake make libuuid-devel python-devel gcc
RUN yum -y install python-qpid-proton qpid-proton-c-devel
ADD qpid-dispatch-0.4.tar.gz /
RUN cd qpid-dispatch-0.4; mkdir build
RUN cd /qpid-dispatch-0.4/build; cmake -DCMAKE_INSTALL_PREFIX=/usr ..
RUN cd /qpid-dispatch-0.4/build; make install
ADD hub.conf /etc/qpid-dispatch/
ADD capsule.conf /etc/qpid-dispatch/
EXPOSE 5672
CMD bash

