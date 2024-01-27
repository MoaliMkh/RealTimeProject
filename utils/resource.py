class Resource:
    def __init__(self, name, total_units):
        self.name = name
        self.total_units = total_units
        self.allocated_units = 0

    @property
    def free_units_count(self):
        return self.total_units - self.allocated_units
