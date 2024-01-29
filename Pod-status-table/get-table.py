import subprocess
from tabulate import tabulate
from datetime import datetime
import time

# Initialize the data list
data = []

while True:
    # Run the 'kubectl top pod' command
    result_top = subprocess.run(['kubectl', 'top', 'pod'], stdout=subprocess.PIPE)

    # Decode the output and split it into lines
    lines_top = result_top.stdout.decode('utf-8').splitlines()

    # Check if there is no data from 'kubectl top pod'
    if len(lines_top) <= 1:
        print("No data from 'kubectl top pod'")
        time.sleep(5)  # wait for 5 seconds before the next iteration
        continue

    # The first line is the header
    header_top = lines_top[0].split()

    # The rest of the lines are the data
    new_data_top = [line.split() for line in lines_top[1:]]

    # Run the 'kubectl get pods' command
    result_get = subprocess.run(['kubectl', 'get', 'pods'], stdout=subprocess.PIPE)

    # Decode the output and split it into lines
    lines_get = result_get.stdout.decode('utf-8').splitlines()

    # The rest of the lines are the data
    new_data_get = [line.split() for line in lines_get[1:]]

    # Process the new data
    for row_top in new_data_top:
        job_name = row_top[0]

        # If the job name already exists in the data, update the row
        for existing_row in data:
            if existing_row[0] == job_name:
                existing_row[1:3] = row_top[1:3]  # update CPU and memory
                break
        else:
            # If the job name does not exist in the data, add a new row
            row_top.append('N/A')  # initial duration
            data.append(row_top)

    # Update the 'Duration' column with data from 'kubectl get pods'
    for row_get in new_data_get:
        job_name = row_get[0]
        status = row_get[2] 
        duration = row_get[-1]

        # Find the corresponding row in the data and update the duration
        for existing_row in data:
            if existing_row[0] == job_name:
                if status == 'Running':
                    existing_row[-1] = duration
                break

    # Generate the table
    table = tabulate(data, headers=header_top + ['Duration'], tablefmt="fancy_grid")

    print(table)

    time.sleep(5)  # wait for 5 seconds before the next iteration