


class Component():
    def __init__(self):
        self.info = {}
        super().__init__()


class InputText():
    def setValue(self, value):
        self.info.update({
            "value":value
        })
    def __init__(self, info):
        self.info = info
    

class Choice():
    def __init__(self, choieList):
        super().__init__()
        self.choiceList = choiceList


