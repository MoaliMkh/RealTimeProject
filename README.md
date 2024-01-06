# Project Documentation

## Overview

This project is a real-time systems simulation for a flight management system. It includes tasks with different levels of criticality and shared resources. The project is implemented in Python.

The main components of the project are:

- Task: A class that represents a task in the system. Each task has a name, deadline, execution time, resource, criticality level, and other attributes.
- Resource: A class that represents a resource in the system. Each resource has a total number of units and allocated units.
- er_edf_stack_resource: A function that implements the EDF-ER (Earliest Deadline First with Enhanced Resources) scheduling algorithm. This function schedules tasks based on their deadlines and resource requirements.

## How to Run

To run the project, follow these steps:

1. Ensure that you have Python installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

2. Clone the project repository to your local machine using the following command:

git clone <repository_url>

3. Navigate to the project directory:

cd <project_directory>

4. Run the main script:

python main.py

This will start the simulation and you will see the scheduling results in the console.

## Logging

The project uses Python's built-in logging module to log the execution of the scheduling algorithm. The log messages provide information about the processing of tasks, resource allocation, and other key events.

The log messages are written to a file named er_edf_stack_resource.log in the same directory as the Python script.

## Contributing

Contributions to the project are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate unit tests.