from utils.er_edf import ErEDF
from utils.task import TaskGenerator, BaseTask
import json


class Runner:

    @staticmethod
    def run():
        all_tasks = []
        all_resources = []
        data = TaskGenerator().generate_task_and_resource_set()
        tasks = data['tasks'] # type:  list['BaseTask']
        resources = data['resources']

        ErEDF(tasks, resources).schedule()

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
                "should_schedule_later": task.should_schedule_later
            })

        for resource in resources:
            all_resources.append({
                "name": resource.name,
                "total_units": resource.total_units,
                "allocated_units": resource.allocated_units
            })

        with open('all_tasks.json', 'w') as fout:
            json.dump(all_tasks, fout, indent=4)

        with open('all_resources.json', 'w') as fout:
            json.dump(all_resources, fout, indent=4)
        print(tasks)
        all_LC_tasks = 0
        counter = 0
        for task in tasks:
            # if task.criticality == "LC":
            #     all_LC_tasks += 1
            if task.finish_time != None:
                counter += 1

        # print(all_LC_tasks)
        print(len(tasks))
        print(counter)


Runner.run()
