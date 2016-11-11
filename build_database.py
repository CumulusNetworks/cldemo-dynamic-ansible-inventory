#!/usr/bin/env python

import redis
conn = redis.Redis('localhost')

leaf01 = '{ \
    "settings": {"ansible_user": "cumulus", "ansible_ssh_pass": "CumulusLinux!", "ansible_become_pass": "CumulusLinux!"} \
    "interfaces": {"lo": "10.1.1.1/32", "swp1": ""}, \
    "bgp": {"asn": "65412", "peers": ["swp1"]}}'
spine01 = '{ \
    "settings": {"ansible_user": "cumulus", "ansible_ssh_pass": "CumulusLinux!", "ansible_become_pass": "CumulusLinux!"} \
    "interfaces": {"lo": "10.2.2.2/32", "swp1": ""}, \
    "bgp": {"asn": "65413", "peers": ["swp1"]}}'

conn.set("leaf01", leaf01)
conn.set("spine01", spine01)
