#!/usr/bin/env python

import redis
import argparse
import json

conn = redis.Redis('localhost')

parser = argparse.ArgumentParser()
parser.add_argument('--host', action='store')
args = parser.parse_args()

if args.host:
    return json.loads(conn.get("inventory"))
else:
    return {'_meta': {'hostvars': {}}}


#redis_string = conn.get("leaf02")

# blah = json.loads(redis_string)

# print blah["lo"]

# inventory = '{ \
#     "network": { \
#         "hosts": ["spine01", "leaf01"], \
#         "vars": { \
#             "ansible_user": "cumulus", \
#             "ansible_ssh_pass": "CumulusLinux!", \
#             "ansible_become_pass": "CumulusLinux!" \
#         } \
#     } \
# }'
