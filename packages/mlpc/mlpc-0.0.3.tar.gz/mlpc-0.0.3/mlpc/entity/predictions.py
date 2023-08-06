from mlpc.entity.base_entity import BaseEntity


class Predictions(BaseEntity):
    def __init__(self, log, storage):
        super().__init__(log, storage)

    def save(self, predictions):
        self._log.debug("Saving predictions")