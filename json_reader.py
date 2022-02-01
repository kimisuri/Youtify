import json
import os


class Json(dict):
    def __init__(self, filename, default=None):
        if default is None:
            default = {}

        if os.path.exists(filename):
            with open(filename, encoding="utf8") as f:
                temp = json.load(f)
        else:
            with open(filename, "w", encoding="utf") as f:
                temp = default
                json.dump(temp, f)

        super().__init__(temp)
        self.filename = filename

    def set(self, value: dict):
        self.clear()
        for key, val in value.items():
            self[key] = val

    def commit(self):
        with open(self.filename, "w", encoding="utf8") as f:
            json.dump(self, f)
