import glob
import json
import matplotlib.pyplot as plt

class Reporter:
    def __init__(self, report_dir='data'):
        self._report_dir = report_dir

    

    def read_files(self):
        generated_tasks_before_run = []
        generated_tasks_after_run = []

        all_resources = []

        for index, filename in enumerate(glob.glob('data/*')):
            if 'before_run' in filename:
                with open(filename, 'r+') as f:
                    data = json.load(f)
                    generated_tasks_before_run.append(data)
            if 'after_run'in filename:
                with open(filename, 'r+') as f:
                    data = json.load(f)
                    generated_tasks_after_run.append(data)

            if 'resources'in filename:
                with open(filename, 'r+') as f:
                    data = json.load(f)
                    all_resources.append(data)
            
        return (generated_tasks_before_run, generated_tasks_after_run, all_resources)

    def process_tasks_data(self, simulations):
        results = []

        for simulation in simulations:
            counter = 0
            for task in simulation:
                if task['finish_time'] is not None:    
                    counter += 1
            results.append((counter, len(simulation)))
        
        return results



    def draw(self, x, y, label):
        print(x)
        print(y)

        plt.plot(x, y)
        plt.title(label=label)
        plt.show()

    
    def report(self):
        simulations = self.read_files()
        before_run_tasks = self.process_tasks_data(simulations[0])
        X_for_before_run = []
        Y_for_before_run = []

        for index, result in enumerate(before_run_tasks):
            X_for_before_run.append(index + 1)
            Y_for_before_run.append(result[0] / result[1])
            
        self.draw(X_for_before_run, Y_for_before_run, "Before")

        after_run_tasks = self.process_tasks_data(simulations[1])
        X_for_after_run = []
        Y_for_after_run = []

        for index, result in enumerate(after_run_tasks):
            X_for_after_run.append(index + 1)
            Y_for_after_run.append(result[0]/result[1])
            
        self.draw(X_for_after_run, Y_for_after_run, "After")
            
        


reporter = Reporter()
reporter.report()