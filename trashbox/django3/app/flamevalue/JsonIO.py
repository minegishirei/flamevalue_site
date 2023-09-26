
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

class JsonDictionalyManager():
    def __init__(self, folder = "/flamevalue"):
        self.folder = folder
        self.jsonIO = JsonIO(folder)
    
    def generate_all_flameworkdict(self):
        directory = glob.glob(f"{self.folder}/*")
        flameworkdict = []
        for filename in os.listdir(path=f'{self.folder}'):
            name = filename.replace(".json", "")
            row = self.jsonIO.read(name)
            new_row = {
                "basic" : row["basic"],
                "score" : row["score"],
                "name" : name,
                "stars" : row["stars"],
                "total_score" : row["total_score"],
                "image" : row["image"],
                "explain" : row["explain"],
                "admin_comment" : row.get("admin_comment")
            }
            flameworkdict.append(new_row)
        return flameworkdict
