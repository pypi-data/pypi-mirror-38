from mlpc.entity.base_entity import BaseEntity


class Model(BaseEntity):
    def __init__(self, log, storage):
        super().__init__(log, storage)

    def save(self, trained_model):
        self._log.debug("Saving trained model")