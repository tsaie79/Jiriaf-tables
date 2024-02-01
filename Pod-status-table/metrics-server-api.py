from kubernetes import client, config
from tabulate import tabulate

# Load the kube config from the default location (i.e., ~/.kube/config)
config.load_kube_config()

# Create an API client for the Metrics API
v1beta1api = client.CustomObjectsApi()


# list all the available metrics
nodes = v1beta1api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
pods = v1beta1api.list_namespaced_custom_object("metrics.k8s.io", "v1beta1", "kube-system", "pods")

node_table = []
for node in nodes['items']:
    table = []
    table.append(node['metadata']['name'])
    table.append(node['usage']['cpu'])
    table.append(node['usage']['memory'])
    node_table.append(table)

print(tabulate(node_table, headers=["Node", "CPU", "Memory"]))

pods_table = []
for pod in pods['items']:
    table = []
    table.append(pod['metadata']['name'])
    table.append(pod['containers'][0]['usage']['cpu'])
    table.append(pod['containers'][0]['usage']['memory'])
    pods_table.append(table)

print(tabulate(pods_table, headers=["Pod", "CPU", "Memory"]))
