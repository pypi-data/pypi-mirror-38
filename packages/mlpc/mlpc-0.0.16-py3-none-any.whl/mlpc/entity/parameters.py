import json
from mlpc.entity.base_entities import BaseEntity


class _ParameterValues:
    def __init__(self):
        pass

    def __getitem__(self, item):
        return self.__dict__[item]


class ParameterReader:
    def load_from_json(self, config_file_path):
        def _obj_encoder(dct):
            pv = _ParameterValues()
            for k in dct:
                setattr(pv, k, dct[k])
            return pv

        assert isinstance(config_file_path, str)
        with open(config_file_path, 'r') as json_file:
            values_dict = json.load(json_file, object_hook=_obj_encoder)
        return values_dict


class Parameters(BaseEntity):
    def __init__(self, storage):
        super().__init__(storage)

    load_from_json = ParameterReader().load_from_json

    def save(self, parameter_values, parameter_set_name="parameters"):
        class ParameterValuesEncoder(json.JSONEncoder):
            def default(self, obj):
                import inspect
                if inspect.isclass(type(obj)):
                    return obj.__dict__
                return json.JSONEncoder.default(self, obj)
        assert isinstance(parameter_set_name, str)
        file_path = self._storage.get_filepath_for_writing("parameters", parameter_set_name, "json")
        with open(file_path, 'w') as json_file:
            json.dump(parameter_values, json_file, cls=ParameterValuesEncoder, indent=4)
        return file_path
