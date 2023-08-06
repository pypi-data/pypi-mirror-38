import json


class Model(object):
    id_keys = []

    def __init__(self, client):
        self._client = client
        super().__init__()

    def load(self):
        self._lazy_load_all()
        return self

    def __repr__(self):
        return "<{module_name}.{class_name}({keys}) object at {hash}>".format(
            module_name=self.__module__,
            class_name=self.__class__.__name__,
            keys=','.join(map(
                lambda k: k + '=' + json.dumps(getattr(self, k)),
                self.id_keys
            )),
            hash=hex(id(self))
        )
