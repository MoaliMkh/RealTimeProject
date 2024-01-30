import glob
import json
import matplotlib.pyplot as plt

class Reporter:
    def __init__(self, report_dir='data'):
        self._report_dir = report_dir

    def read_files(self):
        generated_tasks_before_run = []
        generated_tasks_after_run = []

        QoSTasks = []

        for index, filename in enumerate(glob.glob('data/*')):
            if 'before_run' in filename:
                with open(filename, 'r+') as f:
                    data = json.load(f)
                    generated_tasks_before_run.append(data)
            if 'after_run'in filename:
                with open(filename, 'r+') as f:
                    data = json.load(f)
                    generated_tasks_after_run.append(data)

            if 'after_run'in filename:
                with open(filename, 'r+') as f:
                    data = json.load(f)
                    QoSTasks.append(data)
            
        return (generated_tasks_before_run, generated_tasks_after_run, QoSTasks)

    def process_tasks_data(self, simulations):
        results = []

        for simulation in simulations:
            counter = 0
            for task in simulation:
                if task['finish_time'] is not None:    
                    counter += 1
            results.append((counter, len(simulation)))
        
        return results
    

    def process_QoSTasks(self, simulations):
        results = []
        for simulation in simulations:
            counter = 0
            whole_length = 0
            for task in simulation:
                if task['criticality'] == "LC":
                    whole_length += 1
                    if task['finish_time'] is not None:    
                        counter += 1
            results.append((counter, whole_length))
        
        return results



    def draw(self, x, y, label):
        print(x)
        print(y)

        plt.plot(x, y)
        plt.title(label=label)
        plt.show()

    
    def report(self):
        simulations = self.read_files()
        QoSTasks = self.process_QoSTasks(simulations[2])
        X_for_QoS = []
        Y_for_QoS = []

        for index, result in enumerate(QoSTasks):
            X_for_QoS.append(index + 1)
            Y_for_QoS.append(result[0] / result[1])
            
        self.draw(X_for_QoS, Y_for_QoS, "Quality of Service Analysis")

        after_run_tasks = self.process_tasks_data(simulations[1])
        X_for_schedulability = []
        Y_for_schedulability = []

        for index, result in enumerate(after_run_tasks):
            X_for_schedulability.append(index + 1)
            Y_for_schedulability.append(result[0]/result[1])
            
        self.draw(X_for_schedulability, Y_for_schedulability, "Schedulability Analysis")
            
        


reporter = Reporter()
reporter.report()