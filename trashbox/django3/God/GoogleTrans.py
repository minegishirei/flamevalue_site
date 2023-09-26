from googletrans import Translator
import requests
translator = Translator()



def en_to_ja(text):
    url = "https://script.google.com/macros/s/AKfycbwcAgSR9hDpZ-v2s_71oib44zdT-HDMtVbo0QjksIdJix8p41GWm3FD4sJ_zRUvXDAb/exec"
    payload = {
        "text":text, 
        "source":"en", 
        "target": "ja"
        }
    r = requests.get(url, params=payload)
    return r.json()["text"]



"""
def en_to_ja(text):
    translated = translator.translate(text, dest="ja")
    return translated.text

"""