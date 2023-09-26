from django.test import TestCase

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://twitter.com/xtremepentest/status/1530558904752652289"
# Create your tests here.
html = urlopen(url)

bsObj = BeautifulSoup(html)

print(bsObj)

