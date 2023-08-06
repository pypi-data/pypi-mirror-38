from mlpc.entity.base_entities import BaseEntity
from mlpc.utils.log import debug
from mlpc.metadata import METADATA_FILENAME
import os
import shutil


class Code(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    def copy_code(self, source_folder, collection_name, file_types_to_copy=None):
        if file_types_to_copy is None:
            file_types_to_copy = ["py"]

        def ignore(folder_path, file_and_folder_names):
            ignore_list = []
            for file_or_folder_name in file_and_folder_names:
                full_path = os.path.abspath(os.path.join(folder_path, file_or_folder_name))
                file_type = os.path.splitext(full_path)[1].replace(".", "")
                is_mlpc_root = os.path.exists(os.path.join(full_path, METADATA_FILENAME))
                is_file = os.path.isfile(full_path)
                not_ok_file_type = file_type not in file_types_to_copy
                if (is_file and not_ok_file_type) or is_mlpc_root:
                    ignore_list.append(file_or_folder_name)
            return ignore_list

        assert isinstance(source_folder, str)
        target_folder = self._storage.get_folderpath_for_writing("code", collection_name)
        target_folder = os.path.join(target_folder, "files")
        debug("Copying files from '" + source_folder + "' to '" + str(target_folder) + "'")
        shutil.copytree(source_folder, target_folder, ignore=ignore)
        return target_folder
