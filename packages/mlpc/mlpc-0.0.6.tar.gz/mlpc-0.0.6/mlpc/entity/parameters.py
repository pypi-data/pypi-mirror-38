from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import info


class Parameters(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, parameters):
        info("Saving parameters")