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
import argparse

PROMPT = ['#', '>']
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
    child.sendline('config t')
    child.expect(PROMPT)
    return child

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
    snmpauth = args.snmpaut
    snmppriv = args.snmppriv
    snmpencrypt = args.snmpencrypt

    if hosts:
        for line in hosts:
            host = line.rstrip()
            child = connect(user, host, passwd, en_passwd)
            send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
            send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth + PRIVCMD + snmpencrypt + ' ' + snmppriv)
            send_command(child, SNMPSRVHOSTCMD + ' ' + snmphost + VERSION3CMD + + PRIVCMD + snmpuser)
            send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
            send_command(child, SNMPSRVENTRAP)
            send_command(child, ENDCMD)
            send_command(child, WRME)

    elif host:
        child = connect(user, host, passwd, en_passwd)
        send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
        send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth + PRIVCMD + snmpencrypt + ' ' + snmppriv)
        send_command(child, SNMPSRVHOSTCMD + ' ' + snmphost + VERSION3CMD + PRIVCMD + snmpuser)
        send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
        send_command(child, SNMPSRVENTRAP)
        send_command(child, ENDCMD)
        send_command(child, WRME)
    else:
        print ('Specify either --host or --host_file or I have nothing to do')

if __name__ == '__main__':
    main()