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
            debug("Creating run folder:", new_folder)
            os.mkdir(new_folder)
        return new_folder

    def get_filepath_for_writing(self, entity_type, file_name, file_type):
        folder_path = os.path.join(self.run_path, entity_type)
        self._create_folders_if_needed(folder_path)
        file_path = os.path.join(folder_path, file_name)
        file_path_with_number = self._get_unique_path(file_path, file_type)
        open(file_path_with_number, 'a').close()  # Create empty file to avoid collisions if writes are delayed
        debug("Creating file for writing:", file_path_with_number)
        return file_path_with_number

    def get_folderpath_for_writing(self, entity_type, resource_name):
        folder_path = os.path.join(self.run_path, entity_type, resource_name)
        folder_path_with_number = self._get_unique_path(folder_path)
        self._create_folders_if_needed(folder_path_with_number)
        debug("Creating folder for writing:", folder_path_with_number)
        return folder_path_with_number

    def save_resource(self, entity_type, resource_name, resource_content):
        file_path = self.get_filepath_for_writing(entity_type, resource_name, None)
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

    def _get_unique_path(self, path, file_type=None, suffix_number=1):
        path_with_number_and_file_type = \
            path + \
            "." + str(suffix_number) + \
            (("." + file_type) if len(file_type or "") > 0 else "")
        if os.path.exists(path_with_number_and_file_type):
            return self._get_unique_path(path, file_type, suffix_number=suffix_number + 1)
        return path_with_number_and_file_type

    @staticmethod
    def _check_if_folder_exists(path):
        abspath = os.path.abspath(path)
        if not os.path.isdir(abspath):
            raise ValueError("Folder does not exist: '" + abspath + "'. Set a valid root folder.")
