from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import debug


class Model(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, trained_model):
        debug("TODO: Saving trained model")