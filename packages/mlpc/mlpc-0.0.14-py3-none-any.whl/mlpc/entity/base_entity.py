from mlpc.storage.folderstorage import FolderStorage


class BaseEntity:
    def __init__(self, storage):
        assert isinstance(storage, FolderStorage)
        self._storage = storage
