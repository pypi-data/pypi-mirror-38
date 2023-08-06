from mlpc.entity.base_entities import BaseEntity
from mlpc.utils.log import debug


class Code(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    # def save_running_code(self, folder, extension="py"):
    #     debug("TODO: Saving running code under folder", folder, "with extension", extension)
