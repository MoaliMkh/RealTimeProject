import random
from copy import deepcopy

from .criticality_levels import CRITICALITY_LEVELS
from .task import HC, LC, TaskResource, CriticalSection
from utils.resource import Resource
from .uunifast import uunifast


class TaskGenerator:

    def __init__(
            self,
            total_resource_count=15,
            resource_min_unit_count=1,
            resource_max_unit_count=5,
            total_task_count=100,
            critical_sections_min_count=6,
            critical_sections_max_count=10,
            total_utilization=0.5,
    ):
        self._total_resource_count = total_resource_count
        self.resource_min_unit_count = resource_min_unit_count
        self.resource_max_unit_count = resource_max_unit_count

        self._total_task_count = total_task_count
        self._critical_sections_min_count = critical_sections_min_count
        self._critical_sections_max_count = critical_sections_max_count

        self._total_utilization = total_utilization

    @staticmethod
    def _generate_hc_task(
            index: int,
            name: str,
            period: int,
            utilization: float,
            critical_sections: list['CriticalSection'],
    ) -> HC:
        long_execution_time = utilization * period
        short_execution_time = random.uniform(0.01, long_execution_time)

        return HC(
            name=name,
            release_time=index * period,
            critical_sections=critical_sections,
            exec_time=short_execution_time,
            long_exec_time=long_execution_time,
            period=period,
        )

    @staticmethod
    def _generate_lc_task(
            index: int,
            name: str,
            period: int,
            utilization: float,
            critical_sections: list['CriticalSection'],
    ) -> LC:
        execution_time = utilization * period

        return LC(
            name=name,
            release_time=index * period,
            critical_sections=critical_sections,
            period=period,
            exec_time=execution_time,
        )

    def _generate_critical_sections_for_task(self, execution_time, resources: list['Resource']):
        all_sections = []
        critical_sections_count = random.randint(self._critical_sections_min_count, self._critical_sections_max_count)
        for _ in range(critical_sections_count):
            original_resource = random.choice(resources)
            task_resource = TaskResource(
                original_resource=original_resource,
                units=random.randint(1, original_resource.total_units)
            )

            critical_section_duration = random.uniform(0.01, execution_time)

            relative_start_time = random.uniform(
                0,
                execution_time - critical_section_duration
            )

            relative_end_time = relative_start_time + critical_section_duration

            section = CriticalSection(
                relative_start_time=relative_start_time,
                relative_end_time=relative_end_time,
                task_resource=task_resource,
            )
            all_sections.append(section)

        return all_sections

    def generate_all_resources(self):
        resources = []
        for i in range(self._total_resource_count):
            resource = Resource(
                name=i,
                total_units=random.randint(self.resource_min_unit_count, self.resource_max_unit_count),
            )
            resources.append(resource)
        return resources

    @staticmethod
    def _gen_execution_time(utilizations, i, period):
        return period * utilizations[i]

    def generate_task_and_resource_set(self):
        resources = self.generate_all_resources()
        tasks = []
        hc_periods = [
            5,
            10,
            15,
        ]
        lc_periods = [
            5,
            10,
            15,
        ]
        all_periods = hc_periods + lc_periods
        utilizations = uunifast(len(all_periods), self._total_utilization)

        task_period_count = int(self._total_task_count / (len(all_periods)))

        hc_critical_sections = [
            self._generate_critical_sections_for_task(
                execution_time=self._gen_execution_time(utilizations, i=i, period=period),
                resources=resources
            ) for i, period in enumerate(hc_periods)
        ]

        lc_critical_sections = [
            self._generate_critical_sections_for_task(
                execution_time=self._gen_execution_time(utilizations, i=len(hc_periods) + i, period=period),
                resources=resources
            ) for i, period in enumerate(lc_periods)
        ]

        for index in range(task_period_count):
            for i, period in enumerate(hc_periods):
                tasks.append(
                    self._generate_hc_task(
                        index=index,
                        name=f'{index}-{i}',
                        utilization=utilizations[i],
                        period=period,
                        critical_sections=deepcopy(hc_critical_sections[i]),
                    )
                )
            for i, period in enumerate(lc_periods):
                tasks.append(
                    self._generate_lc_task(
                        index=index,
                        name=f'{index}-{i}',
                        utilization=utilizations[len(hc_periods) + i],
                        period=period,
                        critical_sections=deepcopy(lc_critical_sections[i]),
                    )
                )

        return dict(
            tasks=tasks,
            resources=resources
        )
