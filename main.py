from utils.er_edf import ErEDF
from utils.task import TaskGenerator


class Runner:

    @staticmethod
    def run():
        data = TaskGenerator().generate_task_and_resource_set()
        tasks = data['tasks']
        resources = data['resources']
        ErEDF(tasks, resources).schedule()


Runner.run()
