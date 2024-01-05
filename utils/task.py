class Task:
    def __init__(self, name, deadline, short_exec_time, long_exec_time, resource, criticality,
                 critical_section_units):
        self.name = f'{name}-{criticality}'
        self.deadline = deadline
        self.short_exec_time = short_exec_time
        self.long_exec_time = long_exec_time
        self.final_exec_time = short_exec_time
        self.exec_time = 0
        self.resource = resource
        self.criticality = criticality
        self.is_scheduled = False
        self.critical_section_units = critical_section_units

    def is_schedulable(self, current_time):
        return current_time + self.exec_time <= self.deadline and not self.is_scheduled

    def __lt__(self, other):
        return self.deadline < other.deadline

    def __repr__(self):
        return f'Task {self.name} with deadline {self.deadline} and execution time {self.exec_time}'
