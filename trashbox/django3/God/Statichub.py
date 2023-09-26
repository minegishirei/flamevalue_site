import os


def does_exists(filepath):
    return os.path.exists(filepath)


def write(filepath,text):
    with open(filepath, "w") as f:
        f.write(text)
