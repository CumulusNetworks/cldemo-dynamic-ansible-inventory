#!/usr/bin/env python

# Requires pip install redis
import redis
conn = redis.Redis('localhost')

'''
The easiest way to manage the ansible info within redis
is to turn the vars yaml file into a python dict.

But redis is funky about how it handles complex datastructures (like nested dicts).
The easy solution is treat it all like JSON.

Each device has a string of settings.

That string is loaded into redis can then can be modified through python.

Since this is a demo around reading inventory and settings from an external source,
no effort was put into making adding/modifying nodes easier.
'''
inventory = '{ \
    "network": { \
        "hosts": ["spine01", "leaf01"], \
        "vars": { \
            "ansible_user": "cumulus", \
            "ansible_ssh_pass": "CumulusLinux!", \
            "ansible_become_pass": "CumulusLinux!" \
        } \
    } \
}'


leaf01 = '{ \
    "settings": {"ansible_user": "cumulus", "ansible_ssh_pass": "CumulusLinux!", "ansible_become_pass": "CumulusLinux!"}, \
    "interfaces": {"lo": "10.1.1.1/32", "swp1": ""}, \
    "bgp": {"asn": "65412", "peers": ["swp1"]}}'
spine01 = '{ \
    "settings": {"ansible_user": "cumulus", "ansible_ssh_pass": "CumulusLinux!", "ansible_become_pass": "CumulusLinux!"}, \
    "interfaces": {"lo": "10.2.2.2/32", "swp1": ""}, \
    "bgp": {"asn": "65413", "peers": ["swp1"]}}'

conn.set("leaf01", leaf01)
conn.set("spine01", spine01)
conn.set("inventory", inventory)
