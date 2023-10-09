import json

def get_api_keys(filepath):
    with open(filepath, "r") as file:
        keys = json.load(file)
    return keys
