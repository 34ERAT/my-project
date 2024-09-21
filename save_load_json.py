import json
import os

def save_json(path:str,data):
    with open(path,'w') as file:
        json.dump(data,file,indent=4)
        file.close()

def load_json(path:str):
    if not os.path.exists(path=path):
        save_json(path=path,data=[])
    with open(path,'r',encoding='utf-8') as file:
        data = json.load(file)
        file.close()
    return data

