
from xml.etree import ElementTree
import pprint
import requests


def get_wikipedia_list():
    url = "https://ja.wikipedia.org/w/api.php?format=json&callback=foobar&action=query&list=categorymembers&cmlimit=500&cmtitle=Category:%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9E&format=xml"
    res = requests.get(url)
    res_text = res.text
    elem = ElementTree.fromstring(res_text)
    wiki_list = []
    for child in elem[1][0]:
        wiki_list.append({
            "name" : child.attrib["title"].replace(" (プログラミング言語)", "言語"),
            "wikipedia_name" : child.attrib["title"]
        })
    return wiki_list

pprint.pprint(get_wikipedia_list())
