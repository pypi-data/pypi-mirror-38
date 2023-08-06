import time
from mlpc.entity.code import Code
from mlpc.entity.data import Data
from mlpc.entity.measurements import Measurements
from mlpc.entity.model import Model
from mlpc.entity.parameters import Parameters
from mlpc.entity.plot import Plot
from mlpc.entity.predictions import Predictions
from mlpc.entity.version import Version
from mlpc.runs.base_run import BaseRun
from mlpc.storage.folderstorage import FolderStorage
from mlpc.utils.log import info

class TrainingRun(BaseRun):
    def __init__(self):
        super().__init__()
        self._run_start_timestamp = time.time()
        self.version = Version()
        self._storage = FolderStorage(self.version)
        self.data = Data(self._storage)
        self.parameters = Parameters(self._storage)
        self.measurements = Measurements(self._storage)
        self.plot = Plot(self._storage)
        self.model = Model(self._storage)
        self.code = Code(self._storage)
        self.predictions = Predictions(self._storage)

    def start(self):
        info("New training run started.", "Timestamp:", self.version.timestamp)

    def complete(self, produce_report=True):
        duration_seconds = time.time() - self._run_start_timestamp
        info(
            "Training run completed.",
            "Time elapsed:", str(round(duration_seconds, 3)) + "s.",
            "Resourced saved:", self._storage.number_of_files_written, "(" + str(self._storage.total_bytes_written) + " bytes).",
            "Folder: '" + self._storage.run_abs_path + "'"
        )
        # TODO Produce report
        # TODO Save logging output
