from mlpc.entity.base_entity import BaseEntity


class Measurements(BaseEntity):
    def __init__(self, log, storage):
        super().__init__(log, storage)

    def save(self, measurement_name, measurement):
        self._log.debug("Saving measurement")
