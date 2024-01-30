import heapq

from utils.logger import logger
from utils.task import HC, BaseTask


class ErEDF:
    def __init__(self, tasks, resources):
        self._tasks = tasks
        self._resources = resources
        self._is_overrun = False
        # we can change this
        self._overrun_time = 10
        self.x = 1.5

    def _schedule(self):
        current_time = 0
        task_queue = []
        for task in self._tasks:
            heapq.heappush(task_queue, task)

        current_task = None

        while task_queue:
            if all([_.should_schedule_later for _ in task_queue]):
                # impossible
                logger.info('Schedule is not feasible. deadlock detected!!!')
                break

            task = heapq.heappop(task_queue)

            if task != current_task and current_task is not None:
                new_task_critical_sections = [
                    cs for cs in task.critical_sections
                ]
                old_task_critical_sections = [
                    cs for cs in current_task.critical_sections
                ]

                new_task_original_resources = set([
                    cs.task_resource.original_resource for cs in task.critical_sections
                ])

                old_task_original_resources = set([
                    cs.task_resource.original_resource for cs in current_task.critical_sections
                ])


                if not all(
                    cs.task_resource.original_resource.free_units_count >= cs.task_resource.units
                    for cs in new_task_critical_sections
                ) and new_task_original_resources.issubset(old_task_original_resources):
                    for cs in old_task_critical_sections:
                        cs.task_resource.release_resources()

            current_task = task

            current_time, task = self._get_current_running_task(current_time, task)
            task.should_schedule_later = False

            if current_time >= self._overrun_time and not self._is_overrun:
                self._is_overrun = True
                # Check if the task has reached its short execution time and if it's a high criticality task,
                # switch to long execution time
                for task in self._tasks:
                    if isinstance(task, HC) and task.finish_time is None:
                        task.exec_time = task.long_exec_time
                        task.period = task.period * self.x
                        if task.executed_time != 0:
                            task.release_time = task.release_time * self.x

            # Check if the task has reached its deadline
            if current_time >= task.deadline:
                if isinstance(task, HC):
                    logger.info(f'Task {task} has missed its deadline')
                    logger.info('Schedule is not feasible!')
                    return False
                else:
                    continue

            current_critical_sections = [
                cs for cs in task.critical_sections if
                cs.relative_start_time <= task.executed_time < cs.relative_end_time
            ]

            # Check if the task has access to all resources it needs
            if all(
                    cs.task_resource.original_resource.free_units_count >= cs.task_resource.units
                    for cs in current_critical_sections
            ):
                # Utilize resources
                for cs in current_critical_sections:
                    cs.task_resource.acquire_resources()
            else:
                # Release task to retry later
                # we set this true to prevent infinite loop
                task.should_schedule_later = True
                heapq.heappush(task_queue, task)
                continue

            # Mark the task as running and update the task's execution time
            duration = min([0.1, task.exec_time - task.executed_time])
            task.executed_time += duration
            current_time += duration

            # Check if the task has completed its execution
            if task.executed_time >= task.exec_time:
                task.finish(current_time)
                # Release all resources held by the task
                for cs in task.critical_sections:
                    cs.task_resource.release_resources()
            else:
                current_task = task
                # we add it back to queue to continue execution
                heapq.heappush(task_queue, task)

        logger.info('Schedule is feasible')
        return True

    @staticmethod
    def _get_current_running_task(current_time, r_task: BaseTask):
        if r_task.release_time > current_time:
            current_time = r_task.release_time
        return current_time, r_task

    def schedule(self):
        return self._schedule()
