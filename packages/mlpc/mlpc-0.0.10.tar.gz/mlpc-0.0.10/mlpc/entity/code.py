from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import debug


class Code(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save_running_code(self):
        debug("Saving running code")