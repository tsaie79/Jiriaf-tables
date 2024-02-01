import time
from kubernetes import client, config
from tabulate import tabulate

# Load the kube config from the default location (i.e., ~/.kube/config)
config.load_kube_config()
# Create an API client for the Metrics API
v1beta1api = client.CustomObjectsApi()

# Crate an API client for the Core API
v1 = client.CoreV1Api()

def get_node_metrics():
    nodes = v1beta1api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    node_table = []
    for node in nodes['items']:
        table = []
        table.append(node['metadata']['name'])
        cpu = node['usage']['cpu']
        if cpu[-1:] == 'n':
            table.append(int(cpu[:-1]) / 1000000000)
        elif cpu[-1:] == 'u':
            table.append(int(cpu[:-1]) / 1000000)
        elif cpu[-1:] == 'm':
            table.append(int(cpu[:-1]) / 1000)
        else:
            table.append(int(cpu))

        memory = node['usage']['memory']
        if memory[-2:] == 'Ki':
            table.append(int(memory[:-2]) * 1024)
        elif memory[-2:] == 'Mi':
            table.append(int(memory[:-2]) * 1024 * 1024)
        elif memory[-2:] == 'Gi':
            table.append(int(memory[:-2]) * 1024 * 1024 * 1024)
        else:
            table.append(memory)

        node_table.append(table)
    print(tabulate(node_table, headers=["Node", "CPU", "Memory"]))



def get_pod_metrics():
    pods = v1beta1api.list_namespaced_custom_object("metrics.k8s.io", "v1beta1", "default", "pods")
    pods_table = []
    for pod in pods['items']:
        # sum the cpu and memory usage of all containers in the pod
        cpu = 0
        memory = 0
        for container in pod['containers']:
            if container['usage']['cpu'][-1:] == 'n':
                cpu += int(container['usage']['cpu'][:-1]) / 1000000000
            elif container['usage']['cpu'][-1:] == 'u':
                cpu += int(container['usage']['cpu'][:-1]) / 1000000
            elif container['usage']['cpu'][-1:] == 'm':
                cpu += int(container['usage']['cpu'][:-1]) / 1000
            else:
                cpu += int(container['usage']['cpu'])

            if container['usage']['memory'][-2:] == 'Ki':
                memory += int(container['usage']['memory'][:-2]) * 1024
            elif container['usage']['memory'][-2:] == 'Mi':
                memory += int(container['usage']['memory'][:-2]) * 1024 * 1024
            elif container['usage']['memory'][-2:] == 'Gi':
                memory += int(container['usage']['memory'][:-2]) * 1024 * 1024 * 1024
            else:
                memory += int(container['usage']['memory'])

        pods_table.append([pod['metadata']['name'], cpu, memory])
    print(tabulate(pods_table, headers=["Pod", "CPU", "Memory"]))


def get_pod_status():
    ret = v1.list_namespaced_pod("default")
    table = []
    for i in ret.items:
        table.append([i.metadata.name, i.status.phase])
        

def main():
    while True:
        get_node_metrics()
        get_pod_metrics()
        get_pod_status()
        time.sleep(5)

if __name__ == "__main__":
    main()
