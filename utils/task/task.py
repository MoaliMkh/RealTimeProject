from typing import List, Union
from .criticality_levels import CriticalityLevels


class TaskResource:
    def __init__(self, original_resource, units):
        self.units = units
        self.original_resource = original_resource
        self.is_acquired = False

    def release_resources(self):
        if self.original_resource.allocated_units < self.units and self.is_acquired:
            raise ValueError('Cannot release more units than allocated')
        if self.is_acquired:
            self.is_acquired = False
            self.original_resource.allocated_units -= self.units

    def acquire_resources(self):
        if self.is_acquired:
            return
        self.is_acquired = True
        self.original_resource.allocated_units += self.units


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
        self.name = name
        self.release_time = release_time
        self.executed_time = 0
        self.exec_time = exec_time
        self.criticality = criticality
        self.is_scheduled = False
        self.critical_sections = critical_sections
        self.period = period
        self.finish_time = None
        self.should_schedule_later = False

    @property
    def deadline(self):
        return self.release_time + self.period

    def finish(self, time):
        self.finish_time = time

    def __lt__(self, other):
        return (
                (
                        self.deadline < other.deadline
                ) and not self.should_schedule_later
        )

    def __repr__(self):
        return f'index: {self.name}\n' + \
            f'criticality: {self.criticality}\n' + \
            f'period: {self.period}\n' + \
            f'exec_time: {self.exec_time}\n' + \
            f'release_time: {self.release_time}\n' + \
            f'finish_time: {self.finish_time}'


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
