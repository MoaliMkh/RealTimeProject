import random
from utils import Resource, er_edf_stack_resource, uunifast


class Runner:

    def run(self):
        n = 100
        u = 1
        criticality_levels = ['HC', 'LC']
        period = 10

        # Generate the task set using the UUniFast algorithm
        tasks = uunifast(n, u, criticality_levels, period)
        n_resources = 15
        resources = [
            Resource(random.randint(1, 5))
            for _ in range(n_resources)
        ]

        # Run the simulation
        er_edf_stack_resource(tasks, resources)


Runner().run()
