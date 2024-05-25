import os
import json

def load_json_to_argument(json_path: str):
    # Load the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def write_to_json(data: dict, json_path: str):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

