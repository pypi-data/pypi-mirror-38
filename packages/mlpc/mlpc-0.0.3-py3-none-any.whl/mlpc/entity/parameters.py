from mlpc.entity.base_entity import BaseEntity


class Parameters(BaseEntity):
    def __init__(self, log, storage):
        super().__init__(log, storage)

    def save(self, parameters):
        self._log.debug("Saving parameters")