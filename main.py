from utils.er_edf import ErEDF
from utils.task import TaskGenerator, BaseTask
import json


class Runner:

    @staticmethod
    def serializer_tasks(tasks, f_name):
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

        with open(f'{f_name}.json', 'w') as f_out:
            json.dump(all_tasks, f_out, indent=4)

    @classmethod
    def run(cls):

        data = TaskGenerator().generate_task_and_resource_set()
        tasks = data['tasks']  # type:  list['BaseTask']
        resources = data['resources']

        cls.serializer_tasks(tasks, 'all_tasks_before_run')

        all_serialized_resources = []
        for resource in resources:
            all_serialized_resources.append({
                "name": resource.name,
                "total_units": resource.total_units,
                "allocated_units": resource.allocated_units
            })

        with open('all_resources.json', 'w') as f_out:
            json.dump(all_serialized_resources, f_out, indent=4)

        ErEDF(tasks, resources).schedule()

        cls.serializer_tasks(tasks, 'all_tasks_after_run')

        print(tasks)
        all_LC_tasks = 0
        counter = 0
        for task in tasks:
            # if task.criticality == "LC":
            #     all_LC_tasks += 1
            if task.finish_time is not None:
                counter += 1

        # print(all_LC_tasks)
        print(len(tasks))
        print(counter)


Runner.run()
