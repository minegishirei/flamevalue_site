
import glob
import os
import json

class JsonIO():
    def __init__(self, folder = "/flamevalue"):
        self.folder = folder
    def read(self,name):
        with open(self.folder + "/" + name + ".json", 'r') as f:
            return json.loads(f.read())
    def write(self, name, python_dict):
        with open(self.folder + "/" + name + ".json", 'w+') as f:
            json.dump(python_dict, f, indent=2, ensure_ascii=False)
    def exists(self, name):
        return os.path.isfile(self.folder + "/" + name + ".json")
