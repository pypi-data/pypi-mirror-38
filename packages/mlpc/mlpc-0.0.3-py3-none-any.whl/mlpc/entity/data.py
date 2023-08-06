from mlpc.entity.base_entity import BaseEntity


class Data(BaseEntity):
    def __init__(self, log, storage):
        super().__init__(log, storage)

    def save(self, dataset_name, dataset):
        self._log.debug("Saving training data")
        self._storage.save_resource("data", dataset_name, dataset)
