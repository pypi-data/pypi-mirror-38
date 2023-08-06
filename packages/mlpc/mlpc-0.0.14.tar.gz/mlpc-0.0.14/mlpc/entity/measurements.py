from mlpc.entity.base_entity import BaseEntity


class Measurements(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, measurement_name, measurement):
        assert isinstance(measurement, float) or isinstance(measurement, int)
        self._storage.save_resource("measurement", measurement_name, str(measurement), "txt")
