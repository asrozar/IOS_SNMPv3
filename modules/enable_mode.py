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
__author__ = 'Avery Rozar'

import pexpect

from modules.prompts import *
from modules.cmds import *


def enable_mode(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:', '.Connection refused.'])

    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT])
        if ret == 0:
            print '[-] Could not accept new key from ' + host
            return
    if ret == 3:
        print '[-] Could not connect to ' + host
        return
    child.sendline(passwd)
    auth = child.expect(['.[P|p]assword:', '.>', '.#'])
    if auth == 0:
        print 'User password for ' + host + ' is incorrect'
        return
    if auth == 1:
        child.sendline('enable')
        child.sendline(en_passwd)
        enable = child.expect([pexpect.TIMEOUT, '.#'])
        if enable == 0:
            print 'enable password for ' + host + ' is incorrect'
            return
        if enable == 1:
            child.sendline(SHOWVER)
            what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.', '.Nexus.'])
            if what_os == 0:
                print 'show ver' + ' time out' + ' for ' + host
                return
            if what_os == 1:  # IOS
                child.sendcontrol('c')
                child.expect(PRIV_EXEC_MODE)
                child.sendline(IOSTERMLEN0)
                child.expect(PRIV_EXEC_MODE)
                return child
            if what_os == 2:  # ASAOS
                child.send(QOUTMORE)
                child.expect(PRIV_EXEC_MODE)
                child.sendline(ASATERMPAGER0)
                child.expect(PRIV_EXEC_MODE)
                return child
            if what_os == 3:  # NX-OS
                child.sendcontrol('c')
                child.expect(PRIV_EXEC_MODE)
                child.sendline(IOSTERMLEN0)
                child.expect(PRIV_EXEC_MODE)
                return child

    if auth == 2:
        child.sendline(SHOWVER)
        what_os = child.expect([pexpect.TIMEOUT,  '.IOS.', '.Adaptive.', '.Nexus.'])
        if what_os == 0:
            print 'show ver' + ' time out' + 'for ' + host
            return
        if what_os == 1:  # IOS
            child.sendcontrol('c')
            child.expect(PRIV_EXEC_MODE)
            child.sendline(IOSTERMLEN0)
            child.expect(PRIV_EXEC_MODE)
            return child
        if what_os == 2:  # ASAOS
            child.send(QOUTMORE)
            child.expect(PRIV_EXEC_MODE)
            child.sendline(ASATERMPAGER0)
            child.expect(PRIV_EXEC_MODE)
            return child
        if what_os == 3:  # NX-OS
            child.sendcontrol('c')
            child.expect(PRIV_EXEC_MODE)
            child.sendline(IOSTERMLEN0)
            child.expect(PRIV_EXEC_MODE)
            return child

    else:
        print 'Failed to log in to ' + host