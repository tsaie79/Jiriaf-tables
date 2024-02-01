# Kubernetes Information Retrieval

This project demonstrates how to use the Kubernetes APIs to retrieve information about the nodes and pods in a cluster.

## Illustration

The package provides a script that continuously fetches and prints the details of the nodes and pods in a Kubernetes cluster. It uses the Kubernetes Python client to interact with the Kubernetes APIs and fetch the required information.

## APIs Used
- `CoreV1Api`: Used to fetch the details of the pods and nodes in the cluster.
- `CustomObjectsApi`: Used to fetch the live metrics of the pods and nodes in the cluster.

## How to use APIs
**CoreV1Api**
```python
from kubernetes import client, config
    # Load the kube config from the default location (i.e., ~/.kube/config)
    config.load_kube_config()
    # Create an API client for the CoreV1 API
    v1 = client.CoreV1Api()
    # Get the list of nodes
    ret = v1.list_node(watch=False)
```
* For more details, refer to the script `coreV1API.py`



***CustomObjectsApi***
```python
from kubernetes import client, config
    # Load the kube config from the default location (i.e., ~/.kube/config)
    config.load_kube_config()
    # Create an API client for the Metrics API
    v1beta1api = client.CustomObjectsApi()
    # Get the metrics of the nodes
    nodes = v1beta1api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
```
* For more details, refer to the script `customObjectsAPI.py`