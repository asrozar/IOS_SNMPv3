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

import getpass
import argparse
from modules.config_mode import *
from modules.send_cmd import *
from modules.cmds import *

PROMPT = ['.#', '.>']
SNMPGROUPCMD = ' snmp-server group '
V3PRIVCMD = ' v3 priv '
SNMPSRVUSRCMD = ' snmp-server user '
V3AUTHCMD = ' v3 auth '
PRIVCMD = ' priv '
SNMPSRVHOSTCMD = ' snmp-server host '
VERSION3CMD = ' version 3 '
SHAHMACCMD = ' sha '
SNMPSRVENTRAP = ' snmp-server enable traps '
SNMPSRVCONTACTCMD = ' snmp-server contact '
ENDCMD = ' end '
WRME = ' write memory '

def main():
    parser = argparse.ArgumentParser('usage %prog ' + '--host --host_file --username --password--enable --group --snmp_user --snmp_host --snmp_contact --snmp_v3_auth --snmp_v3_hmac --snmp_v3_priv --snmp_v3_encr')
    parser.add_argument('--host', dest='host', type=str, help='specify a target host')
    parser.add_argument('--host_file', dest='hosts', type=file, help='specify a target host file')
    parser.add_argument('--username', dest='user', type=str, help='specify a user name')
    parser.add_argument('--password', dest='passwd', type=str, help='specify a passwd')
    parser.add_argument('--enable', dest='en_passwd', type=str, help='specify an enable passwd')
    parser.add_argument('--group', dest='group', type=str, help='specify an snmp group')
    parser.add_argument('--snmp_user', dest='snmpuser', type=str, help='specify an snmp user')
    parser.add_argument('--snmp_host', dest='snmphost', type=str, help='specify an snmp server host')
    parser.add_argument('--snmp_contact', dest='snmpcontact', type=str, help='specify your snmp contact info')
    parser.add_argument('--snmp_v3_auth', dest='snmpauth', type=str, help='specify the snmp user authentication')
    parser.add_argument('--snmp_v3_hmac', dest='snmphmac', type=str, help='set snmp HMAC, md5 or sha')
    parser.add_argument('--snmp_v3_priv', dest='snmppriv', type=str, help='specify the snmp priv password')
    parser.add_argument('--snmp_v3_encr', dest='snmpencrypt', type=str, help='specify encryption, des, 3des, or aes(128/192/256)')

    args = parser.parse_args()
    host = args.host
    hosts = args.hosts
    user = args.user
    passwd = args.passwd
    en_passwd = args.en_passwd
    group = args.group
    snmpuser = args.snmpuser
    snmphost = args.snmphost
    snmpcontact = args.snmpcontact
    snmpauth = args.snmpauth
    snmppriv = args.snmppriv
    snmpencrypt = args.snmpencrypt

    if host is None and hosts is None:
        print('I need to know what host[s] to connect to')
        print parser.usage
        exit(0)

    if user is None:
        user = raw_input('Enter your username: ')

    if passwd is None:
        passwd = getpass.getpass(prompt='User Password: ')

    if en_passwd is None:
        en_passwd = getpass.getpass(prompt='Enable Secret: ')

    if group is None:
        group = raw_input('Enter your SNMP group: ')

    if snmpuser is None:
        snmpuser = raw_input('Enter your SNMP user: ')

    if snmphost is None:
        snmphost = raw_input('Enter your SNMP server address: ')

    if snmpcontact is None:
         snmpcontact = raw_input('Who is your SNMP contact info: ')

    if snmpauth is None:
        snmpauth = raw_input('Enter the SNMP user auth string: ')

    if snmppriv is None:
        snmppriv = raw_input('Enter the SNMP priv string: ')

    if snmpencrypt is None:
        snmpencrypt = raw_input('Enter encryption type | des, 3des, or aes(128/192/256): ')

    if hosts:
        for line in hosts:
            host = line.rstrip()
            child = config_mode(user, host, passwd, en_passwd)

            if child:
                (child, SNMPGROUPCMD + group + V3PRIVCMD)
                send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth + PRIVCMD
                                    + snmpencrypt + ' ' + snmppriv)
                send_command(child, SNMPSRVHOSTCMD + ' ' + snmphost + VERSION3CMD + PRIVCMD + snmpuser)
                send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
                send_command(child, SNMPSRVENTRAP)
                send_command(child, ENDCMD)
                send_command(child, WRME)

    elif host:
        child = config_mode(user, host, passwd, en_passwd)
        send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
        send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth + PRIVCMD +
                            snmpencrypt + ' ' + snmppriv)
        send_command(child, SNMPSRVHOSTCMD + ' ' + snmphost + VERSION3CMD + PRIVCMD + snmpuser)
        send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
        send_command(child, SNMPSRVENTRAP)
        send_command(child, ENDCMD)
        send_command(child, WRME)

if __name__ == '__main__':
    main()