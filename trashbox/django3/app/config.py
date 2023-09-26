import os

ENV = os.environ.get("ENV")
if ENV == "DEV":
    DEBUG = True
else:
    DEBUG = False
print("DEBUG", DEBUG)




