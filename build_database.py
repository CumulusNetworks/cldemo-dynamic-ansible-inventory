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

Ansible expects a group (network) with the hosts and group vars.

The _meta block defines hostvars on a per-host basis.
'''
inventory = """
{
    "network": {
        "hosts": ["spine01", "leaf01", "spine02", "leaf02", "leaf03", "leaf04"],
        "vars": {
            "ansible_user": "cumulus",
            "ansible_ssh_pass": "CumulusLinux!",
            "ansible_become_pass": "CumulusLinux!"
        }
    },
    "_meta": {
        "hostvars": {
            "leaf01": {
                "interfaces": {"lo": "10.1.1.1/32", "swp51": "", "swp52": ""},
                "bgp": {"asn": "65421", "peers": ["swp1", "swp2"]}
            },
            "leaf02": {
                "interfaces": {"lo": "10.1.1.2/32", "swp51": "", "swp52": ""},
                "bgp": {"asn": "65422", "peers": ["swp1", "swp2"]}
            },
            "leaf03": {
                "interfaces": {"lo": "10.1.1.3/32", "swp51": "", "swp52": ""},
                "bgp": {"asn": "65423", "peers": ["swp1", "swp2"]}
            },
            "leaf04": {
                "interfaces": {"lo": "10.1.1.4/32", "swp51": "", "swp52": ""},
                "bgp": {"asn": "65424", "peers": ["swp1", "swp2"]}
            },
            "spine01": {
                "interfaces": {"lo": "10.1.1.111/32", "swp1": "", "swp2": "", "swp3": "", "swp4": ""},
                "bgp": {"asn": "65420", "peers": ["swp1", "swp2", "swp3", "swp4"]}
            }
            "spine02": {
                "interfaces": {"lo": "10.1.1.222/32", "swp1": "", "swp2": "", "swp3": "", "swp4": ""},
                "bgp": {"asn": "65420", "peers": ["swp1", "swp2", "swp3", "swp4"]}
            }

        }
    }
}
"""
conn.set("inventory", inventory)
