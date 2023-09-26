
from bs4 import BeautifulSoup
class HtmlInfo(Compose):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]
        self.elements.update({
            "href" : self.filename
        })
        self.html = ""
        self.title = ""
        self.bsObj = None
        with open(filepath) as f:
            self.html = f.read()
        self.bsObj = BeautifulSoup(self.html)
        #self.__grep_title__()
    
    def seach(self):
        self.asign_to_dict("description")
        self.asign_to_dict("title")
        self.asign_to_dict("sidecolumn")
        self.asign_to_dict("ans")
        self.asign_to_dict("img")
        self.asign_to_dict("xmp")

    def __grep_title__(self):
        self.title = self.bsObj.find("title").get_text()
    
    def asign_to_dict(self, tag):
        tagobj = self.__simple_grep__(tag)
        if tagobj is None:
            return
        if tag=="img":
            self.elements.update({
                tag : tagobj["src"]
            })
        elif tag=="xmp":
            self.elements.update({
                tag : str(tagobj)
            }) 
        else:
            self.elements.update({
                tag : tagobj.get_text()
            }) 

    def __simple_grep__(self, tag):
        return self.bsObj.find(tag)
