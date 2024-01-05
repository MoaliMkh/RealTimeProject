import random

from .task import Task


def uunifast(n, u, criticality_levels, period):
    utilizations = []
    sumU = u
    for i in range(1, n):
        nextSumU = sumU * random.uniform(0, 1) ** (1 / (n - i))
        utilizations.append(sumU - nextSumU)
        sumU = nextSumU
    utilizations.append(sumU)

    task_set = []
    for i in range(n):
        execution_time = utilizations[i] * period
        deadline = period
        criticality = random.choice(criticality_levels)
        if criticality == 'HC':
            short_exec_time = execution_time / 2
            long_exec_time = execution_time
        else:
            short_exec_time = execution_time
            long_exec_time = execution_time
        critical_section_units = random.randint(6, 10)
        task_set.append(
            Task(i, deadline, short_exec_time, long_exec_time, None, criticality, critical_section_units)
        )

    return task_set
