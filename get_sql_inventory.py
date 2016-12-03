#!/usr/bin/env python
'''
This program is designed to be used for Ansible dynamic inventory.

Two arguments are accepted:
 --list to provide all data about all hosts and variables
 --host [hostname] to provide variables for a specific host

All output is returned in valid JSON, with Ansible as an intended consumer.

This inventory script works against a SQLite database.
'''

import sqlite3
import argparse
import json


def query_host_args(hostname):
    '''
    Takes in a hostname string.
    Returns a tuple.

    This method will query a SQLite database running locally
    and pull data about a given hostname that was provided.
    '''

    # This is the name of the local SQLite database file.
    # Expected to be in the current working directory.
    sqlite_file = "ansible_db.sqlite"

    db_connection = sqlite3.connect(sqlite_file)
    c = db_connection.cursor()

    if hostname == "all":
        c.execute('SELECT * from ansible')

    else:
        c.execute('SELECT * FROM ansible WHERE hostname = "' + hostname + '"')

    query_result = c.fetchall()

    if len(query_result) <= 0:
        exit(2)

    # Sqlite fetchall() returns a list of size 1, where the only element is a tuple.
    # It's easier to just return the tuple outside of the list.
    return query_result[0]


def structure_host_output(sql_output):

    '''
    This method takes in a tuple output from query_host_args()
    And returns valid JSON output for that host query
    '''

    '''
    Query Output:
    (u'leaf01', 65421, None, None, None, None, None, None, None, None, None, None, None, 1, 1, None, None, None, None, None, None, None, None, None, None, None, u'', u'', u'10.1.1.1/32')

    JSON Output:
    "leaf01": {
                "interfaces": {"lo": "10.1.1.1/32", "swp51": "", "swp52": ""},
                "bgp": {"asn": "65421", "peers": ["swp51", "swp52"]}
            },
    '''

    # Easiest way to solve the problem was to make a list of all SQL column names.
    keys = ["hostname", "bgp_asn", "swp1_bgp", "swp2_bgp", "swp3_bgp", "swp4_bgp",
            "swp29_bgp", "swp30_bgp", "swp31_bgp", "swp32_bgp", "swp44_bgp", "swp49_bgp",
            "swp50_bgp", "swp51_bgp", "swp52_bgp", "swp1_address", "swp2_address",
            "swp3_address", "swp4_address", "swp29_address", "swp30_address",
            "swp31_address", "swp32_address", "swp44_address", "swp49_address",
            "swp50_address", "swp51_address", "swp52_address", "lo_address"]

    # Then build a dict mapping each column name (as a key) to the returned value from SQLite
    sql_dict = dict(zip(keys, sql_output))
    bgp_peers = []  # In the final output bgp peers is a list of ["peer interface"]
    interfaces = {}  # In the final output interfaces is a dict with {inteface_name: "ip_address"}

    # This uglyiness is because I don't know how to build a proper database schema
    # In order to build the json dict, we loop over all the key names
    # When the value of that key isn't 0, we will put it in the bgp_peers list
    # or the interfaces dict
    for key, value in sql_dict.iteritems():
        if "bgp" in key:  # First see if it's a bgp variable
            if value is not None:  # If the sql query didn't have a value, then there is no peer on that interface
                # we want the interface name from the key, for example swp29_bgp we want "swp29"
                # so strip the _bgp part and put the interface name in the list
                if not key == "bgp_asn":  # without this "bgp_as" will be listed as a peer
                    bgp_peers.append(key[:key.find("_bgp")])

        if "address" in key:  # Now let's look at the interface addresses
            if value is not None:  # None means no address. Empty string ("") means up, but no IP (unnumbered, L2)
                interfaces[key[:key.find("_address")]] = value

    # Build the final dictionary of interfaces + bgp info and
    # Transform the dictionary being built into valid JSON
    return json.dumps({"interfaces": interfaces, "bgp": {"asn": sql_dict["bgp_asn"], "peers": bgp_peers}})


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action='store')
    parser.add_argument('--list', action='store_true')
    return parser.parse_args()


def main():

    args = parse_arguments()

    # The list of hosts in reference topology.
    # If this list changes, be sure to add the new hosts to the SQLite database
    host_list = ["leaf01", "leaf02", "leaf03", "leaf04", "spine01", "spine02"]

    # Called with --host [hostname]
    if args.host:
        query_result = query_host_args(args.host)
        print structure_host_output(query_result)

    # Called with --list
    if args.list:
        hostvars_dict = dict()
        inventory_dict = dict()

        # When called with --list, Ansible expects different output that
        # includes a header, groups and groupvars defined.
        inventory_dict["network"] = {
            "hosts": host_list,
            "vars": {
                "ansible_user": "cumulus",
                "ansible_ssh_pass": "CumulusLinux!",
                "ansible_become_pass": "CumulusLinux!"
            }
        }

        # Loop over every host in the network and get their vars
        for host in host_list:
            query_result = query_host_args(host)
            # structure output has to be cast back to normal dict or
            # building hostvars dict will restult in invalid json
            hostvars_dict[host] = json.loads(structure_host_output(query_result))

        # Build the final dict with groups, groupvars and hostvars
        inventory_dict["_meta"] = {"hostvars": hostvars_dict}

        # Ansible expects data not to be returned by sent to stdout.
        print json.dumps(inventory_dict)
    exit(0)


if __name__ == "__main__":
    main()
