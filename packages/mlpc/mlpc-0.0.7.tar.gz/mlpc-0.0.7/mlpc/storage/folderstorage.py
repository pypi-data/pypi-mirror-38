import os
import time
from mlpc.entity.version import Version
from mlpc.utils.log import debug
import mlpc.configuration


class FolderStorage:
    def __init__(self, version):
        assert isinstance(version, Version)
        self._version = version
        self._check_if_folder_exists(mlpc.configuration.root_folder_path)
        self.run_path = self._create_folder_for_run_and_correct_version()
        self.run_abs_path = os.path.abspath(self.run_path)
        self.number_of_files_written = 0
        self.total_bytes_written = 0

    def _create_folder_for_run_and_correct_version(self):
        new_folder = os.path.join(mlpc.configuration.root_folder_path, self._version.timestamp)
        if os.path.exists(new_folder):
            debug("Version folder already exists. Bumping version and trying again.")
            time.sleep(1)
            self._version.bump_version()  # TODO Use .1 suffixes, this is easier to relate to for humans.
            self._create_folder_for_run_and_correct_version()
        else:
            debug("Creating folder:", new_folder)
            os.mkdir(new_folder)
        return new_folder

    def get_filepath_for_writing(self, entity_type, file_name, file_type):
        folder_path = os.path.join(self.run_path, entity_type)
        self._create_folders_if_needed(folder_path)
        return self._get_new_filename(folder_path, file_name) + "." + file_type

    def get_folderpath_for_writing(self, entity_type, resource_name):
        folder_path = os.path.join(self.run_path, entity_type, resource_name)
        self._create_folders_if_needed(folder_path)
        return folder_path

    def save_resource(self, entity_type, resource_name, resource_content):
        file_path = self.get_filepath_for_writing(entity_type, resource_name)
        self._write_file(file_path, resource_content)
        return file_path

    def _write_file(self, file_path, content):
        debug("Saving file:", file_path)
        with open(file_path, "w") as file:
            file.write(content)
        self.total_bytes_written += os.path.getsize(file_path)
        self.number_of_files_written += 1

    @staticmethod
    def _create_folders_if_needed(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _get_new_filename(self, folder_path, file_name_stem, suffix_number=1):
        file_path = os.path.join(folder_path, file_name_stem + "." + str(suffix_number))
        if os.path.exists(file_path):
            return self._get_new_filename(folder_path, file_name_stem, suffix_number + 1)
        return file_path

    @staticmethod
    def _check_if_folder_exists(path):
        abspath = os.path.abspath(path)
        if not os.path.isdir(abspath):
            raise ValueError("Folder does not exist: '" + abspath + "'. Set a valid root folder.")
