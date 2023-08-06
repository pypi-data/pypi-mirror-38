import mlpc

run = mlpc.new_training_run()

run.code.save_running_code()

train_data = "read some rows with pandas etc"
test_data = "read som other rows with pandas etc"
run.data.save("train", train_data)
run.data.save("test", test_data)

parameters = "{ some: parameter }"  # TODO: run.parameters.read("/path/file.config") ?
run.parameters.save(parameters)

model = "trained model"
run.model.save(model)

measurement1 = "some stats"
run.measurements.save("m1", measurement1)
measurement2 = "some other stats"
run.measurements.save("m2", measurement2)

predictions = "a=1, b=2"
run.predictions.save(predictions)

run.complete()
