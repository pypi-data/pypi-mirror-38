from actions.training import Training


def new_training_run():
    run = Training()
    run.start()
    return run