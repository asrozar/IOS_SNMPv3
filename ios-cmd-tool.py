#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Avery Rozar'
#             ...
#        .:::|#:#|::::.
#     .:::::|##|##|::::::.
#     .::::|##|:|##|:::::.
#      ::::|#|:::|#|:::::
#      ::::|#|:::|#|:::::
#      ::::|##|:|##|:::::
#      ::::.|#|:|#|.:::::
#      ::|####|::|####|::
#      :|###|:|##|:|###|:
#      |###|::|##|::|###|
#      |#|::|##||##|::|#|
#      |#|:|##|::|##|:|#|
#      |#|##|::::::|##|#|
#       |#|::::::::::|#|
#        ::::::::::::::
#          ::::::::::
#           ::::::::
#            ::::::
#              ::

import pexpect

import pxssh
import optparse
import time
from threading import *

PROMPT = ['#', '>',]
UNPROMPT = ['/.U./']
PWPROMPT = ['/.P./']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before

def connect(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])

    if ret == 0:
        print '[-] Error Connecting'
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print '[-] Error Connecting'
            return
    child.sendline(passwd)
    child.expect(PROMPT)
    child.sendline('enable')
    child.sendline(en_passwd)
    child.expect(PROMPT)
    child.sendline('terminal pager 0')
    child.expect(PROMPT)

    return child

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

    child = connect(user, host, passwd, en_passwd)
    send_command(child, cmd)

if __name__ == '__main__':
    main()