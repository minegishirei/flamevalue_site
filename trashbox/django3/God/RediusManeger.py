import redis
import json


cache = redis.StrictRedis(host='redis', port=6379, db=0)
class RediusManeger():
    def __init__(self):
        pass

    def set_pageinfo_list(self, pageinfo_list):
        for info in pageinfo_list:
            cache.set( info["title"],str(info))
    
    def get(self, tag):
        js = json.loads(cache.get(tag))
        js = json.dumps(js, indent = 2, ensure_ascii = False)
        return js
