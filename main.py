import os
import json

from utils.er_edf import ErEDF
from utils.task import TaskGenerator

DATA_DIR = 'data'

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


class Runner:

    def __init__(self, iterations=100):
        self._iterations = iterations

    @staticmethod
    def serializer_tasks(tasks, f_name, index):
        all_tasks = []
        for task in tasks:
            all_tasks.append({
                "name": task.name,
                "release_time": task.release_time,
                "executed_time": task.executed_time,
                "exec_time": task.exec_time,
                "criticality": task.criticality,
                "is_scheduled": task.is_scheduled,
                "period": task.period,
                "finish_time": task.finish_time,
                "should_schedule_later": task.should_schedule_later,
                'critical_sections': [
                    {
                        "relative_start_time": cs.relative_start_time,
                        "relative_end_time": cs.relative_end_time,
                        "task_resource": {
                            "original_resource": {
                                "name": cs.task_resource.original_resource.name,
                                "total_units": cs.task_resource.original_resource.total_units,
                                "free_units_count": cs.task_resource.original_resource.free_units_count
                            },
                            "units": cs.task_resource.units
                        }
                    } for cs in task.critical_sections
                ]
            })

        with open(f'{DATA_DIR}/{f_name}.{index}.json', 'w') as f_out:
            json.dump(all_tasks, f_out, indent=4)

    def _run_single_simulation(self, index):
        data = TaskGenerator().generate_task_and_resource_set()
        tasks = data['tasks']  # type:  list['BaseTask']
        resources = data['resources']

        self.serializer_tasks(tasks, 'all_tasks_before_run', index)

        all_serialized_resources = []
        for resource in resources:
            all_serialized_resources.append({
                "name": resource.name,
                "total_units": resource.total_units,
                "allocated_units": resource.allocated_units
            })

        with open(f'{DATA_DIR}/all_resources-{index}.json', 'w') as f_out:
            json.dump(all_serialized_resources, f_out, indent=4)

        ErEDF(tasks, resources).schedule()

        self.serializer_tasks(tasks, 'all_tasks_after_run', index)

    def run(self):
        for index in range(self._iterations):
            self._run_single_simulation(index)


Runner().run()
