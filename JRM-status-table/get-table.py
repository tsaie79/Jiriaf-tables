from kubernetes import client, config
from tabulate import tabulate

# Configure kubernetes client
config.load_kube_config()

v1 = client.CoreV1Api()

# Get the list of nodes
ret = v1.list_node(watch=False)

# Define the static data
walltime = "1:00:00"
nodetype = "CPU"
site = "Perlmutter"

# Create a list of lists for the table data
table_data = []

for i in ret.items:
    cpu = i.status.capacity['cpu']
    memory = i.status.capacity['memory']
    # conver the memory to GiB
    memory = int(memory[:-2]) / 1024 / 1024 / 1024
    alivetime = i.metadata.labels.get('jiriaf.alivetime', 'N/A')
    name = i.metadata.name

    # Add the data to the table
    table_data.append([name, cpu, memory, walltime, nodetype, site, alivetime])

# Generate the table
table = tabulate(table_data, headers=["Name", "CPU", "Memory", "Walltime", "NodeType", "Site", "AliveTime"], tablefmt="pretty")

print(table)