from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import info


class Data(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, dataset_name, dataset):
        saved_to = self._storage.save_resource("data", dataset_name, dataset)
        info("Saved data:", saved_to)

