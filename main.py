import random
from utils import Resource, er_edf_stack_resource, uunifast


class Runner:

    def run(self):
        n = 10
        u = 1
        criticality_levels = ['HC', 'LC']
        period = 10

        # Generate the task set using the UUniFast algorithm
        tasks = uunifast(n, u, criticality_levels, period)

        resources = [Resource(5), Resource(10)]

        # Run the simulation
        er_edf_stack_resource(tasks, resources)


Runner().run()
