
from github import Github
from urllib.request import urlopen, quote
import urllib
from bs4 import BeautifulSoup
import os
import time
import json


def get_unique_id():
    url = "https://api.countapi.xyz/hit/mysite.com/visits"
    response = urlopen(url).read()
    output = response.decode('utf-8')
    my_dict = json.loads(output)
    return my_dict

def get_unique_id():
    url = "https://api.countapi.xyz/hit/mysite.com/visits"
    response = urlopen(url).read()
    output = response.decode('utf-8')
    my_dict = json.loads(output)
    return my_dict




https://api.countapi.xyz/hit/flamevalue-react/visits
