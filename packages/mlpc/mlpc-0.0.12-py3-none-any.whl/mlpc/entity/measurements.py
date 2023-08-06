from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import debug


class Measurements(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, measurement_name, measurement):
        self._storage.save_resource("measurement", measurement_name, str(measurement), "txt")
