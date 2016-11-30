#!/usr/bin/env python

'''
This script will connect to a SQLite database running on the local machine
and will build a table and populate it with data that represents variables
for the Cumulus reference topology.
'''

import sqlite3

sqlite_file = "ansible_db.sqlite"

db_connection = sqlite3.connect(sqlite_file)
c = db_connection.cursor()

# I will happily accept a PR that builds an actual database schema.
# But until that happens, this demo is about pulling data out of a sql database
# not about proper database schemas.
#
# The simple way I did this was that it's a single table.
# The hostname is a key
# BGP ASN is a string for json simplicity.
# Every possible interface in the reference topology is included
# swp1_bgp defines if it is a bgp unnumbered interface (0 or 1)
# swp1_address defines the IP/mask that is used on the interface.
# The default value for swp1_address is None. If the interface is
# unnumbered or L2 then the value should be an empty string ""

ansible_table_string = """
hostname TEXT PRIMARY KEY,
bgp_asn TEXT,
swp1_bgp INTEGER,
swp2_bgp INTEGER,
swp3_bgp INTEGER,
swp4_bgp INTEGER,
swp29_bgp INTEGER,
swp30_bgp INTEGER,
swp31_bgp INTEGER,
swp32_bgp INTEGER,
swp44_bgp INTEGER,
swp49_bgp INTEGER,
swp50_bgp INTEGER,
swp51_bgp INTEGER,
swp52_bgp INTEGER,
swp1_address TEXT,
swp2_address TEXT,
swp3_address TEXT,
swp4_address TEXT,
swp29_address TEXT,
swp30_address TEXT,
swp31_address TEXT,
swp32_address TEXT,
swp44_address TEXT,
swp49_address TEXT,
swp50_address TEXT,
swp51_address TEXT,
swp52_address TEXT,
lo_address TEXT
"""
c.execute("CREATE TABLE ansible(" + ansible_table_string + ")")

try:
    # Syntax maps keywords to values.
    # Notice ending values are empty strings '' representing unnumbered interfaces
    c.execute("INSERT INTO ansible (hostname, bgp_asn, lo_address, swp51_bgp, swp52_bgp, swp51_address, swp52_address) VALUES ('leaf01', '65421', '10.1.1.1/32', 1, 1, '', '')")
    c.execute("INSERT INTO ansible (hostname, bgp_asn, lo_address, swp51_bgp, swp52_bgp, swp51_address, swp52_address) VALUES ('leaf02', '65422', '10.1.1.2/32', 1, 1, '', '')")
    c.execute("INSERT INTO ansible (hostname, bgp_asn, lo_address, swp51_bgp, swp52_bgp, swp51_address, swp52_address) VALUES ('leaf03', '65423', '10.1.1.3/32', 1, 1, '', '')")
    c.execute("INSERT INTO ansible (hostname, bgp_asn, lo_address, swp51_bgp, swp52_bgp, swp51_address, swp52_address) VALUES ('leaf04', '65424', '10.1.1.4/32', 1, 1, '', '')")
    c.execute("INSERT INTO ansible (hostname, bgp_asn, lo_address, swp1_bgp, swp2_bgp, swp3_bgp, swp4_bgp, swp1_address, swp2_address, swp3_address, swp4_address) VALUES ('spine01', '65420', '10.1.1.111/32', 1, 1, 1, 1, '', '', '', '')")
    c.execute("INSERT INTO ansible (hostname, bgp_asn, lo_address, swp1_bgp, swp2_bgp, swp3_bgp, swp4_bgp, swp1_address, swp2_address, swp3_address, swp4_address) VALUES ('spine02', '65420', '10.1.1.222/32', 1, 1, 1, 1, '', '', '', '')")
except sqlite3.IntegrityError:
    print('ERROR: ID already exists in PRIMARY KEY column {}'.format("hostname"))

db_connection.commit()
db_connection.close()
