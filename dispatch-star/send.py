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

if len(sys.argv) != 4:
    print "Usage: send port address text"
    sys.exit(1)

port    = sys.argv[1]
address = sys.argv[2]
text    = sys.argv[3]

M = proton.Messenger()
M.route("amqp:/*", "amqp://0.0.0.0:%s/$1" % port)
M.start()
msg = proton.Message()
msg.address = address
msg.body    = text
M.put(msg)
M.send()
M.stop()

