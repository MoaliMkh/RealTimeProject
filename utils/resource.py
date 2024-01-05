class Resource:
    def __init__(self, total_units):
        self.name = f'{total_units}'
        self.total_units = total_units
        self.allocated_units = 0

    def allocate_units(self, units):
        self.allocated_units += units

    def release_units(self):
        self.allocated_units = 0
