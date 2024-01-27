from typing import List, Union
from .criticality_levels import CriticalityLevels


class TaskResource:
    def __init__(self, original_resource, units):
        self.units = units
        self.original_resource = original_resource


class CriticalSection:
    def __init__(
            self,
            relative_start_time: float,
            relative_end_time: float,
            task_resource: TaskResource
    ):
        self.relative_start_time = relative_start_time
        self.relative_end_time = relative_end_time
        self.task_resource = task_resource


class BaseTask:

    def __init__(
            self,
            name: Union[int, str],
            release_time: float,
            criticality,
            critical_sections: List[CriticalSection],
            exec_time: float,
            period: int,
    ):
        self.name = f'i:{name}-p:{period}-c:{criticality}'
        self.release_time = release_time
        self.executed_time = 0
        self.exec_time = exec_time
        self.criticality = criticality
        self.is_scheduled = False
        self.critical_sections = critical_sections
        self.period = period

    def is_schedulable(self, current_time):
        return current_time + self.executed_time <= self.deadline and not self.is_scheduled

    @property
    def deadline(self):
        return self.release_time + self.period

    def __lt__(self, other):
        return self.deadline < other.deadline


class HC(BaseTask):
    criticality = CriticalityLevels.HC

    def __init__(
            self,
            name,
            release_time,
            critical_sections: List[CriticalSection],
            exec_time,
            long_exec_time,
            period,
    ):
        super().__init__(name, release_time, self.criticality, critical_sections, exec_time, period)
        self.short_exec_time = exec_time
        self.long_exec_time = long_exec_time


class LC(BaseTask):
    criticality = CriticalityLevels.LC

    def __init__(
            self,
            name,
            release_time,
            critical_sections: List[CriticalSection],
            exec_time,
            period,
    ):
        super().__init__(name, release_time, self.criticality, critical_sections, exec_time, period)
