from mlpc.entity.base_entity import BaseEntity


class Code(BaseEntity):
    def __init__(self, log, storage):
        super().__init__(log, storage)

    def save_running_code(self):
        self._log.debug("Saving running code")