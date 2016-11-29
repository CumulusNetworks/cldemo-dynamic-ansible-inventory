#!/usr/bin/env python

import redis
import argparse
import json


def list_arg(redis_connection):

    return_val = json.loads(redis_connection.get("inventory"))

    # Needs to load then send back to json
    # in order to normalize and make valid

    return json.dumps(return_val)


def host_arg(hostname, redis_connection):
    redis_output = json.loads(list_arg(redis_connection))

    host_vars = redis_output["_meta"]["hostvars"][hostname]
    # Needs to load then send back to json
    # in order to normalize and make valid
    print host_vars
    return json.dumps(host_vars)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action='store')
    parser.add_argument('--list', action='store_true')
    return parser.parse_args()


def main():

    args = parse_arguments()
    redis_connection = redis.Redis('localhost')

    if args.host:
        print host_arg(args.host, redis_connection)
    if args.list:
        print list_arg(redis_connection)


if __name__ == "__main__":
    main()
