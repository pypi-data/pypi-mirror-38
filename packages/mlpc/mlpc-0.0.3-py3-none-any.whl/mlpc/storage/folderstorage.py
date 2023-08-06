class FolderStorage:
    def __init__(self, root_path, log):
        self._root_path = root_path
        self._log = log

    def save_resource(self, entity_type, resource_name, resource_content):
        self._log.debug("Saving file: " + entity_type + "/" + resource_name)