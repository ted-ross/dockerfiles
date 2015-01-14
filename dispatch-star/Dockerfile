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
RUN yum -y install python-qpid-proton qpid-cpp-server qpid-tools
RUN mkdir /demo
RUN mkdir /demo/rpms
ADD libqpid-dispatch-0.3-1.fc21.x86_64.rpm  /demo/rpms/libqpid-dispatch-0.3-1.fc21.x86_64.rpm
ADD qpid-dispatch-router-0.3-1.fc21.x86_64.rpm  /demo/rpms/qpid-dispatch-router-0.3-1.fc21.x86_64.rpm
ADD qpid-dispatch-tools-0.3-1.fc21.x86_64.rpm  /demo/rpms/qpid-dispatch-tools-0.3-1.fc21.x86_64.rpm
RUN rpm -i  /demo/rpms/*.rpm
RUN mkdir /demo/configs
ADD hub.conf /demo/configs/hub.conf
ADD capsule1.conf /demo/configs/capsule1.conf
ADD capsule2.conf /demo/configs/capsule2.conf
ADD capsule3.conf /demo/configs/capsule3.conf
ADD capsule4.conf /demo/configs/capsule4.conf
ADD setup.sh /demo/setup.sh
ADD listen.py /demo/listen.py
ADD send.py /demo/send.py
