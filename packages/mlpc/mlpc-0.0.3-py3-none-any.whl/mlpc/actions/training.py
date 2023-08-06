from mlpc.entity.code import Code
from mlpc.entity.data import Data
from mlpc.entity.measurements import Measurements
from mlpc.entity.model import Model
from mlpc.entity.parameters import Parameters
from mlpc.entity.predictions import Predictions
from mlpc.entity.version import Version
from mlpc.storage.folderstorage import FolderStorage
from mlpc.utils.log import Log


class Training:
    def __init__(self):
        log = Log()
        storage = FolderStorage("/path/to/mlpc_root", log)
        self.version = Version()
        self.data = Data(log, storage)
        self.parameters = Parameters(log, storage)
        self.measurements = Measurements(log, storage)
        self.model = Model(log, storage)
        self.code = Code(log, storage)
        self.predictions = Predictions(log, storage)

    def start(self):
        print("")
        print("New MLPC training run started.")
        print("  Timestamp:", self.version.timestamp)
        print("  Version:", self.version.version)
        print("")

    def complete(self):
        print("")
        print("MLPC training run completed")
        print("  Time elapsed: 1234")
        print("  Resources saved: 7 (1,4GiB)")
        print("  Folder: /path/to/run")
        print("")
