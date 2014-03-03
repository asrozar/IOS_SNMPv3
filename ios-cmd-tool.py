#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
(C) Copyright [2014] InfoSec Consulting, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

         ...
    .:::|#:#|::::.
 .:::::|##|##|::::::.
 .::::|##|:|##|:::::.
  ::::|#|:::|#|:::::
  ::::|#|:::|#|:::::
  ::::|##|:|##|:::::
  ::::.|#|:|#|.:::::
  ::|####|::|####|::
  :|###|:|##|:|###|:
  |###|::|##|::|###|
  |#|::|##||##|::|#|
  |#|:|##|::|##|:|#|
  |#|##|::::::|##|#|
   |#|::::::::::|#|
    ::::::::::::::
      ::::::::::
       ::::::::
        ::::::
          ::
"""

import optparse
from modules.enable_mode import *
from modules.send_cmd import *

PROMPT = ['#', '>',]
UNPROMPT = ['/.U./']
PWPROMPT = ['/.P./']


def main():
    parser = optparse.OptionParser('usage %prog ' + '-H <host> -u <user> -p <passwd> -e <en_passwd> -c <command>')
    parser.add_option('-H', dest='host', type='string', help='specify a target host')
    parser.add_option('-u', dest='user', type='string', help='specify a user name')
    parser.add_option('-p', dest='passwd', type='string', help='specify a passwd')
    parser.add_option('-e', dest='en_passwd', type='string', help='specify an enable passwd')
    parser.add_option('-c', dest='cmd', type='string', help='specify a command')

    (options, args) = parser.parse_args()
    host = options.host
    user = options.user
    passwd = options.passwd
    en_passwd = options.en_passwd
    cmd = options.cmd

    if host is None or passwd is None or user is None or en_passwd is None or cmd is None:
        print parser.usage
        exit(0)

    child = enable_mode(user, host, passwd, en_passwd)
    send_command(child, cmd)

if __name__ == '__main__':
    main()