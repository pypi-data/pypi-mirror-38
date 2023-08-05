# ElasticSearchPy

## About
ElasticSeachPy is a python library used to connect to and interact with elasticsearch

This library is a python implementation of the Elasticsearch HTTP [API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html) and an alternative to ElasticSearch's Python [Library](https://elasticsearch-py.readthedocs.io/en/master/api.html)

## Installation
ElasticSearchPy can be install with the pip distribution system for Python by issuing:
```
$ pip3 install elasticsearch-python-client
```
Alternatively, you can run use setup.py to install by cloning this repository and issuing:
```
$ python3 setup.py install
```

## Limitations
This library is currently under development and is not as feature rich as it will be.  This being said, it currently has several limitations
* **Python3+ Only** - My primary development environment is python3, I currently do not have the time to test and vet interoperability between python2 and python3
* **ElasticSearch Authentication** - Currently, this library only supports "No Authentication" and "SSL w/ Certificate Authentication".  This limitation is simply due to my testing environments
* **Limited Functionality** - If functionality isn't listed here, it is either not implemented or is not tested.  As time moves forward, I will continue to add fuctionality

## Contributors
If you are interested in contributing to this project, feel free to contact me at jeff@koebane.net

## Examples
### Connecting to ElasticSearch
```python
from elasticsearchpy import ElasticSearchConnection
es_ip = "192.168.1.1"
# Connect to the cluster
es_conn = ElasticSearchConnection(es_ip)
# Connect to the cluster with a non 9200 port
# es_conn = ElasticSearchConnection(es_ip, port=80)
# Alternatively Connect to the cluster using SSL certificates
# es_conn = ElasticSearchConnection(es_ip, port=443,
#    use_ssl=True,
#    cert="/path/to/cert.crt",
#    key="/path/to/key.key"
#)
```

### Interact with the Cluster
```python
from elasticsearchpy import ElasticSearchConnection
es_ip = "192.168.1.1"
# Connect to the cluster
es_conn = ElasticSearchConnection(es_ip)

#Get Cluster Object
es_cluster = es_conn.get_cluster()
# get number of active shards
print("There are {} active shards".format(es_cluster.active_shards))
# Get the number of hosts
total_nodes = es_cluster.nodes
data_nodes = es_cluster.data_nodes

print("This cluster has {} nodes ( {} data nodes )".format(total_nodes,data_nodes))

# Get Node Names
nodes = es_cluster.node_names
print("This cluster has the following nodes:")
for node_name in nodes:
  print("- {}".format(node_name))
```

### Interact with a cluster node
```python
from elasticsearchpy import ElasticSearchConnection

es_ip = "192.168.1.1"

# Connect to the cluster
es_conn = ElasticSearchConnection(es_ip)

#Get Cluster Object
es_cluster = es_conn.get_cluster()

# Get Node Names
nodes = es_cluster.node_names

# Get Node Object
node = es_cluster.get_node(nodes[0)

print("Node {}".format(node.name)
if node.master:
    print("* Is the master Node")
if node.ingest_node:
    print("* Is an ingest Node")
if node.data_node:
    print("* Is a data node")

print("Elasticsearch Version: {}".format(node.version))
print("OS: {}".format(node.os))
print("Has the following roles")
print("------------------------")
for role in node.roles:
  print(" - {}".format(role))
```

### Interact with indices
```python
from elasticsearchpy import ElasticSearchConnection

es_ip = "192.168.1.1"

# Connect to the cluster
es_conn = ElasticSearchConnection(es_ip)

# Get Indices Object
non_sys_indices = es_conn.get_indices() # this gets all non-system indices
all_indices = es_conn.get_indices(system_indices=True) # this gets all indices including system indices
bob_indices = es_conn.get_indices(indice_prefix="bob") # this gets all indices that start with bob

# List indices
print("Here are the non-system indices")
for indice in non_sys_indices.indices:
  print("- {}".format(indice)
print("Total: {}".format(non_sys_indices.count)

# Create an indice
my_indice = indices.create_indice("bob-1") # Creates bob-1 with default shard replica values
my_indice2 = indices.create_indice("bob-2", shards=2, replicas=0) # Creates bob-2 with 2 shards and 0 replicas

# Delete an indice
indices.delete_indice("bob-2") # Deletes the Indice named bob-2
```
### Interact with a single indice
```python
from elasticsearchpy import ElasticSearchConnection
from elasticsearchpy import ElasticSearchIndice

es_ip = "192.168.1.1"

# Connect to the cluster
es_conn = ElasticSearchConnection(es_ip)

# Get Indices Object
non_sys_indices = es_conn.get_indices() # this gets all non-system indices

# Get the Indice Object
my_indice = non_sys_indice.get_indice("bob-1") # Retrieves an indice object from the indice bob-1

# Alternative way of getting the Indice Object
my_indice_2 = ElasticSearchIndice("bob-2",es_conn)

print("Indice {} has the following properties".format(my_indice.name))
print("- Status: {}".format(my_indice.status))
print("- Health: {}".format(my_indice.health))
print("- Number of documents: {}".format(my_indice.docs))
print("- Size: {}".format(my_indice.size))

doc_data = {
  "message":"I am a test message",
  "user":"test user",
  "purpose":"TESTING...DUUU"
}
# Creating Documents
doc = my_indice.create_doc(doc_data) # this creates a do and lets elasticsearch generate the id
doc = my_indice.create_doc(doc_data,name="document-1234") # this creates a document that you generate the id for

# Deleting Documents
my_indice.delete_doc("document-1234")
```

## Immediate future TODO List
* Add document search to indice object
* Add templates
* Document documents object