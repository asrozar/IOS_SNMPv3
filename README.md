IOS SNMP v3 tool
=====

This tool bulk edits IOS devices for SNMP v3, priv mode only.

Uses:

You have a few options.

To get help use the -h argument.

python ios-snmpv3-tool.py -h

The minimum arguments are only -—host or --host_file, you will be prompted for the other augments.

python ios-snmpv3-tool.py —-host_file

Use all arguments at once (Less secure, passwords will be loaded on the screen). You will need to use ‘quotes’ in arguments that include special characters and spaces.

python ios-snmpv3-tool.py --host_file=asa.hosts --username=USERNAME —-password='PASSWORD' enable='EN_PASSWORD' --group=SNMPGROUP --snmp_host=10.17.5.19 --snmp_user=SNMPMGR --snmp_v3_auth='$nmpM@n@g3rAUTH' --snmp_v3_priv='$nmpM@n@g3rPRIV' --snmp_v3_encr='aes 128'  --snmp_contact='Wile E. Coyote | wile.e.coyote@acme.com'

Use most arguments, you will be prompted for the other augments.

python ios-snmpv3-tool.py --host_file=asa.hosts --username=USERNAME --group=SNMPGROUP --snmp_host=10.17.5.19 --snmp_user=SNMPMGR --snmp_v3_auth='$nmpM@n@g3rAUTH' --snmp_v3_priv='$nmpM@n@g3rPRIV' --snmp_v3_encr='aes 128'  --snmp_contact='Wile E. Coyote | wile.e.coyote@acme.com'
