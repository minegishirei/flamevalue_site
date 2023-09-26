import json

class MyLocalJson():
    def __init__(self, filepath):
        self.filepath = filepath
        self.jsondict = {}
        self.jsonstr = ""
        with open(self.filepath) as f:
            self.jsonstr = f.read()
            self.jsondict = json.loads(self.jsonstr)
    
    def read(self):
        return self.jsondict
    
    def write(self, new_jsondict):
        text = json.dumps(new_jsondict, ensure_ascii=False, indent=4)
        with open(self.filepath, "w") as f:
            f.write(text)

class MyJson():
    def __init__(self):
        pass

    def read(self, jsonstr):
        self.jsonstr = jsonstr
        self.jsondict = json.loads(self.jsonstr)
        return self.jsondict
    
    def write(self, new_jsondict):
        text = json.dumps(new_jsondict, ensure_ascii=False, indent=4)
        return text
