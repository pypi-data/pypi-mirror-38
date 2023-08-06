from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import info


class Model(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, trained_model):
        info("Saving trained model")