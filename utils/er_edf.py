import heapq

from .logger import logger


def resource_that_task_can_acquire(task, resources):
    for resource in resources:
        if resource.total_units - resource.allocated_units >= task.critical_section_units:
            return resource
    return None


def er_edf_stack_resource(tasks, resources):
    # Create a heap of tasks sorted by their deadlines
    active_tasks = []
    for task in tasks:
        heapq.heappush(active_tasks, (task.deadline, task))
    time = 0

    while active_tasks:
        current_task = heapq.heappop(active_tasks)[1]
        logger.info('Processing task %s with deadline %s', current_task.name, current_task.deadline)

        if current_task.resource not in resources:
            for task in tasks:
                if task.resource == current_task.resource and not task.is_scheduled:
                    if task.resource is not None:
                        resources.append(task.resource)
                        task.resource.release_units()
                        logger.info('Resource %s released by task %s', task.resource.name, task.name)
                        task.resource = None

                    break
        else:
            resources.remove(current_task.resource)
            current_task.resource.allocate_units(current_task.critical_section_units)
            logger.info('Resource %s acquired by task %s', current_task.resource, current_task.name)

        current_task.is_scheduled = True

        current_task.exec_time += 1
        logger.info('Task %s execution time is %s', current_task.name, current_task.exec_time)

        if current_task.criticality == 'HC' and current_task.exec_time > current_task.short_exec_time:
            current_task.final_exec_time = current_task.long_exec_time
            logger.info('Task %s switched to long execution time', current_task.name)

        if current_task.exec_time >= current_task.deadline:
            logger.info('Task %s reached its deadline', current_task.name)
            if not current_task.is_scheduled:
                current_task.is_scheduled = True

                logger.info('Checking if any tasks with late deadlines can be scheduled')
                while active_tasks:
                    next_task = heapq.heappop(active_tasks)[1]

                    if next_task.deadline > time:
                        heapq.heappush(active_tasks, (next_task.deadline, next_task))
                        break

        else:
            active_tasks.append((current_task.deadline, current_task))
            l_resource = resource_that_task_can_acquire(current_task, resources)
            if current_task.resource is None and l_resource is not None:
                resources.remove(l_resource)
                current_task.resource = l_resource
                current_task.resource.allocate_units(current_task.critical_section_units)
                logger.info('Resource %s acquired by task %s', current_task.resource.name, current_task.name)

            else:
                logger.info('Task %s does not need any resources', current_task.name)
                pass

        if current_task.exec_time >= current_task.final_exec_time:
            logger.info('Task %s completed its execution', current_task.name)
            active_tasks.remove((current_task.deadline, current_task))
            if current_task.resource:
                logger.info('Task %s released all resources', current_task.name)
                resources.append(current_task.resource)
                current_task.resource.release_units()
                current_task.resource = None

        time += 1

    logger.info('Finished er_edf_stack_resource function')
    return tasks
