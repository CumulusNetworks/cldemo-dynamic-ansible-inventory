# cldemo-dynamic-ansible-inventory

This demo shows how an external datasource can be used to populate all variable and host information at runtime.

There are two examples within this demo, one utilizes a redis datastore as the external source, the other utilizes SQLite as an external SQL database.

This demo is built using the Cumulus Networks [reference topology](https://github.com/cumulusnetworks/cldemo-vagrant)

![Cumulus Reference Topology](https://github.com/CumulusNetworks/cldemo-vagrant/raw/master/cldemo_topology.png)

Quickstart
------------------------
* git clone https://github.com/cumulusnetworks/cldemo-vagrant
* cd cldemo-vagrant
* vagrant up
* vagrant ssh oob-mgmt-server
* sudo su - cumulus
* git clone *<URL>*
* cd cldemo-dynamic-ansible-inventory
* ansible-playbook redis_setup.yml
* ansible all -m ping -i get_redis_inventory.py
* ansible-playbook provision_network.yml -i get_redis_inventory.py

Details
------------------------
Once this repo has been cloned to the out of band management server you can build one or both of the databases.

Once either database is installed and populated with data (which is done as part of the install playbook),

*Demo Redis*
First, install the redis database with `ansible-playbook redis_setup.yml`. This step will also populate the redis database with the network variables.
Next, you can test without a provided inventory and see that Ansible fails. This command is `ansible all -m ping`
To test by pulling the host information out of Redis use `ansible all -m ping -i get_redis_inventory.py`.
Once the ping is successful, you can configure the network with `ansible-playbook provision_network -i get_redis_inventory.py`
*Note:* If the Redis demo was previously run, please reset the lab with `ansible-playbook reset.yml -i get_sql_inventory.py`

You can verify that the network was provisioned correctly with `ansible spine01 -a 'vtysh -c "show ip bgp sum"' -i get_redis_inventory.py --become`. 2 BGP peers should appear.

*Demo SQL*
First, install the SQLite database with `ansible-playbook sql_setup.yml`. This step will also populate the SQL database with the network variables. When the database is created, SQLite will create a file in the current directory called "ansible.sl".

*Note:* This demo will fail if ansible.sl is not in the same directory that the `ansible` commands are being executed from.

Next, we can test a ping without a provided inventory file with `ansible all -m ping`.

Now, providing an inventory, we can test the ping again using `ansible all -m ping -i get_sql_inventory.py`, which will work.

Finally, the network can be configured with `ansible-playbook provision_network.yml -i get_sql_inventory.py`.
*Note:* If the Redis demo was previously run, please reset the lab with `ansible-playbook reset.yml -i get_sql_inventory.py`

You can verify that the network was provisioned correctly with `ansible spine01 -a 'vtysh -c "show ip bgp sum"' -i get_sql_inventory.py --become`. 2 BGP peers should appear.
