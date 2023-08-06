from mlpc.entity.base_entity import BaseEntity
from mlpc.utils.log import debug


class Model(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def save(self, trained_model):
        debug("TODO: Saving trained model")

    def get_filepath_for_writing(self, model_name, file_type):
        return self._storage.get_filepath_for_writing("model", model_name, file_type)