from mlpc.runs.training_run import TrainingRun
import mlpc.configuration
import logging

do_not_configure_logging = False

def new_training_run():
    if (not do_not_configure_logging):
        logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    run = TrainingRun()
    run.start()
    return run