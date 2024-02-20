#!/usr/bin/env python3

import os

elastic_ver = "8.12.1"
elastic_net = "elastic"
img_src = "docker.io/library"
es = f"{img_src}/elasticsearch:{elastic_ver}"
kb = f"{img_src}/kibana:{elastic_ver}"
runtime = "docker"

# Create elastic network
create_net = f"{runtime} network create {elastic_net}"
net_id, exit_stat = os.system(create_net)

# Pull elastic image from docker hub
pull_es = f"{runtime} pull {es}"
pull_kb = f"{runtime} pull {kb}"
os.system(pull_es)
os.system(pull_kb)

# Start elasticsearch container
es_name = "es-test-01"
mem_lim = "2GB"
start_es = f"{runtime} run --name {es_name} --net {elastic_net} -p 9200:9200 -it -m {mem_lim} {es}"
os.system(start_es)

# Create tokens
token_type = "kibana"  # inputs: kibana, node
es_bin = "/usr/share/elasticsearch/bin"
es_token = f"{runtime} exec -it {es_name} {es_bin}/elasticsearch-create-enrollment-token -s {token_type}"


# Start kibana container
kb_name = "kb-test-01"
start_kb = f"{runtime} run --name {kb_name} --net {elastic_net} -p 5601:5601 {kb}"
os.system(start_kb)

# Add elasticsearch node container
node_name = "es-test-02"
token = input("Elastic enrollment token:\n")
new_es_node = f"{runtime} run -e 'ENROLLMENT_TOKEN={token}' --name {node_name} --net {elastic_net} -m {mem_lim} {es} -d"
os.system(new_es_node)
