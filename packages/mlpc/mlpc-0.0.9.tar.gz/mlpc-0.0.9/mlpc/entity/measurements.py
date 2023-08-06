from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import info


class Measurements(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, measurement_name, measurement):
        info("Saving measurement")
