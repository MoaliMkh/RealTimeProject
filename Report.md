# er_edf.py Documentation

The er_edf.py file is a key part of the project, implementing the EDF-ER (Earliest Deadline First with Enhanced Resources) scheduling algorithm for real-time systems. This file contains the following functions:

## resource_that_task_can_acquire(task, resources)

This function checks if a task can acquire a resource from the available resources. It iterates over the resources and returns the first resource that the task can acquire based on its critical section units. If no such resource is found, it returns None.

## er_edf_stack_resource(tasks, resources)

This is the main function in the file, implementing the EDF-ER scheduling algorithm. It takes a list of tasks and resources as input.

The function starts by creating a heap of tasks sorted by their deadlines. It then enters a loop that continues until all tasks have been processed.

In each iteration of the loop, the function:

- Retrieves the task with the earliest deadline.
- Checks if the task needs a resource and if the resource is available. If the resource is not available, it checks if any tasks holding it are done and releases the resource back to the stack. If the resource is available, it acquires it.
- Marks the task as running and updates the task's execution time.
- Checks if the task has reached its short execution time and if it's a high criticality task, switches to long execution time.
- Checks if the task has reached its deadline. If it has, it releases the task if not already released and checks if any tasks with late deadlines can be scheduled.
- Checks if the task has access to all resources it needs. If the task has all resources, it utilizes them. If the task doesn't have all resources, it releases it to retry later.
- Checks if the task has completed its execution. If it has, it releases all resources held by the task.
- Updates the time.

The function logs key events during its execution, such as processing tasks, acquiring and releasing resources, switching to long execution time, reaching deadlines, and completing execution.

The function returns the list of tasks after all have been processed.

# Project Documentation

This project is a real-time systems simulation for a flight management system. It is implemented in Python and includes tasks with different levels of criticality and shared resources. The main components of the project are:

## Task Class

The Task class represents a task in the system. Each task has a name, deadline, execution time, resource, criticality level, and other attributes. The class is defined in the task.py file.

## Resource Class

The Resource class represents a resource in the system. Each resource has a total number of units and allocated units. The class is defined in the resource.py file.

## uunifast Function

The uunifast function is used to generate a set of tasks with a specified total utilization. It is defined in the uunifast.py file. The function takes the number of tasks, total utilization, criticality levels, and period as input parameters. It returns a list of Task objects.

## resource_that_task_can_acquire Function

The resource_that_task_can_acquire function checks if a task can acquire a resource from the available resources. It is defined in the er_edf.py file. The function takes a task and a list of resources as input parameters. It returns a Resource object if the task can acquire a resource, otherwise it returns None.

## er_edf_stack_resource Function

The er_edf_stack_resource function implements the EDF-ER (Earliest Deadline First with Enhanced Resources) scheduling algorithm. It is defined in the er_edf.py file. The function takes a list of tasks and resources as input parameters.

The function starts by creating a heap of tasks sorted by their deadlines. It then enters a loop that continues until all tasks have been processed. In each iteration of the loop, the function retrieves the task with the earliest deadline, checks if the task needs a resource and if the resource is available, marks the task as running, updates the task's execution time, checks if the task has reached its deadline or its execution time, and checks if the task has access to all resources it needs. The function logs key events during its execution.

## Runner Class

The Runner class is used to run the simulation. It is defined in the main.py file. The class has a run method that generates a set of tasks using the uunifast function, and then runs the simulation using the er_edf_stack_resource function.

## Logging

The project uses Python's built-in logging module to log the execution of the scheduling algorithm. The log messages provide information about the processing of tasks, resource allocation, and other key events. The logger is configured in the logger.py file.

## How to Run

To run the project, you need to create an instance of the Runner class and call its run method. This will start the simulation and you will see the scheduling results in the console. The results are also logged to a file named er_edf_stack_resource.log in the same directory as the Python script.