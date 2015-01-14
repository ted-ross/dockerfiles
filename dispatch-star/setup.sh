#!/bin/sh

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

##
## Start the qpid broker
##
qpidd --daemon -p 11000

##
## Configure the broker
##
qpid-config -b 0.0.0.0:11000 add queue queue/dest.1

##
## Start the routers
##
qdrouterd --daemon --config /demo/configs/hub.conf
qdrouterd --daemon --config /demo/configs/capsule1.conf
qdrouterd --daemon --config /demo/configs/capsule2.conf
qdrouterd --daemon --config /demo/configs/capsule3.conf
qdrouterd --daemon --config /demo/configs/capsule4.conf

