from mlpc.entity.base_entity import BaseEntity


class Plot(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def get_filepath_for_writing(self, plot_name, file_type):
        return self._storage.get_filepath_for_writing("plot", plot_name, file_type)
