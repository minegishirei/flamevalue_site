import re
import sys
import json
import requests
from pprint import pprint
import collections

key = "aa3528c39331fcd6654a9134411c2871255f3722b2b03904bbf66c4ae6f07b50"


# coding: utf-8
from goolabs import GoolabsAPI


def get_request(text):
    api = GoolabsAPI(key)

    response = api.morph(sentence=text)
    return response


def get_wordlist(text):
    request = get_request(text)
    wordlist = request["word_list"][0]

    tmp_word_list = []
    for row in wordlist:
        if row[1] == "名詞":
            tmp_word_list.append(row[0])
    c = collections.Counter(tmp_word_list)
    return dict(c.most_common())