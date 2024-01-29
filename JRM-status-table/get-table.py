from kubernetes import client, config
from tabulate import tabulate


import time 

while True:
    # Configure kubernetes client
    config.load_kube_config()

    v1 = client.CoreV1Api()

    # Get the list of nodes
    ret = v1.list_node(watch=False)

    # Create a list of lists for the table data
    table_data = []

    for i in ret.items:
        name = i.metadata.name
        # Update the 'Duration' column with data from 'kubectl get pods'
for row_get in new_data_get:
    job_name = row_get[0]
    status = row_get[2]  # the 'STATUS' column
    duration = row_get[-1]

    # Find the corresponding row in the data and update the duration
    for existing_row in data:
        if existing_row[0] == job_name:
            if status == 'Running':
                existing_row[-1] = duration
            break
        # Get allocatable resources
        if i.status.allocatable.get('cpu', 0)[-1:] == 'm':
            allocatable_cpu = int(i.status.allocatable['cpu'][:-1]) / 1000
        else:
            allocatable_cpu = int(i.status.allocatable['cpu'])


        if type(i.status.allocatable.get('memory', 0)) == int:
            allocatable_memory = i.status.allocatable['memory']
        elif i.status.allocatable.get('memory', 0)[-2:] == 'Ki':
            allocatable_memory = int(i.status.allocatable['memory'][:-2]) * 1024
        elif i.status.allocatable.get('memory', 0)[-2:] == 'Mi':
            allocatable_memory = int(i.status.allocatable['memory'][:-2]) * 1024 * 1024
        elif i.status.allocatable.get('memory', 0)[-2:] == 'Gi':
            allocatable_memory = int(i.status.allocatable['memory'][:-2]) * 1024 * 1024 * 1024
        else:
            allocatable_memory = int(i.status.allocatable['memory'][:-2])


        # Get all pods in the node
        field_selector = f'spec.nodeName={name}'
        pods = v1.list_pod_for_all_namespaces(field_selector=field_selector).items

        # Calculate the total CPU and memory requests (allocated resources)
        allocated_cpu = 0
        allocated_memory = 0
        for pod in pods:
            # make sure the pod is running and the node running it is the same as the current node
            if pod.status.phase != 'Running' or pod.spec.node_name != name:
                continue
            print(f"Pod name: {pod.metadata.name}, Node name: {pod.spec.node_name}, Pod status: {pod.status.phase}")
            for container in pod.spec.containers:
                requests = container.resources.requests
                if requests:
                    # convert cpu to cpu not millicpu, and the unit is shown at the end of the string
                    if requests.get('cpu', 0)[-1:] == 'm':
                        allocated_cpu += int(requests.get('cpu', 0)[:-1]) / 1000
                    else:
                        allocated_cpu += int(requests.get('cpu', 0))

                    # Convert memory to bytes depending on the unit (Ki, Mi, Gi), and the unit is shown at the end of the string
                    if type(requests.get('memory', 0)) == int:
                        allocated_memory += requests.get('memory', 0)
                    elif requests.get('memory', 0)[-2:] == 'Ki':
                        allocated_memory += int(requests.get('memory', 0)[:-2]) * 1024
                    elif requests.get('memory', 0)[-2:] == 'Mi':
                        allocated_memory += int(requests.get('memory', 0)[:-2]) * 1024 * 1024
                    elif requests.get('memory', 0)[-2:] == 'Gi':
                        allocated_memory += int(requests.get('memory', 0)[:-2]) * 1024 * 1024 * 1024
                    else:
                        allocated_memory += int(requests.get('memory', 0)[:-2])

        # Calculate available resources
        available_cpu = allocatable_cpu - allocated_cpu
        available_memory = allocatable_memory - allocated_memory

        walltime = i.metadata.labels.get('jiriaf.walltime', 'N/A')
        nodetype = i.metadata.labels.get('jiriaf.nodetype', 'N/A')
        site = i.metadata.labels.get('jiriaf.site', 'N/A')
        alivetime = i.metadata.labels.get('jiriaf.alivetime', 'N/A')

        ## add node's status
        status = "NotReady"
        for condition in i.status.conditions:
            if condition.type == "Ready":
                status = "Ready" if condition.status == "True" else "NotReady"

        # convert memory to Mi and add the unit at the end
        new_memory = {"allocatable_memory": allocatable_memory, "allocated_memory": allocated_memory, "available_memory": available_memory}
        for memory, value in new_memory.items():
            if value < 1024:
                new_memory[memory] = f"{value/1024}Ki"
            elif value < 1024 * 1024:
                new_memory[memory] = f"{value / 1024 / 1024}Mi"
            else:
                new_memory[memory] = f"{value / 1024 / 1024 / 1024}Gi"

        # keep only 2 decimal places
        for memory, value in new_memory.items():
            if value[-2:] == "Ki":
                new_memory[memory] = f"{float(value[:-2]):.2f}Ki"
            elif value[-2:] == "Mi":
                new_memory[memory] = f"{float(value[:-2]):.2f}Mi"
            elif value[-2:] == "Gi":
                new_memory[memory] = f"{float(value[:-2]):.2f}Gi"


        # Add the data to the table
        table_data.append([name, allocatable_cpu, allocated_cpu, available_cpu, new_memory['allocatable_memory'], new_memory['allocated_memory'], new_memory['available_memory'], walltime, nodetype, site, alivetime, status])

    # Generate the table
    table = tabulate(table_data, headers=['Node', 'Total CPU', 'Allocated CPU', 'Available CPU', 'Total Memory', 'Allocated Memory', 'Available Memory', 'Walltime', 'Nodetype', 'Site', 'Alivetime', 'Status'], tablefmt='fancy_grid')

    print(table)

    time.sleep(5)  # wait for 5 seconds before the next iteration

