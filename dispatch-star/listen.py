#!/usr/bin/python

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

import sys
import proton

if len(sys.argv) != 3:
    print "Usage: listen port address"
    sys.exit(1)

port    = sys.argv[1]
address = sys.argv[2]

M = proton.Messenger()
M.route("amqp:/*", "amqp://0.0.0.0:%s/$1" % port)
M.start()
M.subscribe(address)

while (True):
    M.recv(1)
    msg = proton.Message()
    M.get(msg)
    print "Received: %s " % msg.body

