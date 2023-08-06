from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import debug


class Parameters(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, parameters):
        debug("Saving parameters")