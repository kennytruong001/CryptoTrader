import os, json

def getConfigs():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'config.json')
    with open(filename, "r") as f:
        config = json.load(f)
    
    return config