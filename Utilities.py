from json import loads, dumps
from os import makedirs
from os.path import exists as file_exists, join as join_path
import requests
from datetime import datetime


def date_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(message):
    print(f"{date_time()}  |  {message}")

def download_file(url, filename):
    print(url)
    data = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(data)    

def non_char_to_underscore(text):
    check_text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY"
    text = text.strip()
    new_text = ""
    for t in text:
        if t in check_text:
            new_text += t
        else:
            new_text += "_"
    
    return new_text

def create_new_folder(folder_name):
    if not file_exists(folder_name):
        makedirs(folder_name)
    return folder_name

def read_json(file_path):
    output = None
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if lines:
            output = loads("".join(lines))
    return output

def write_json(file_path, object):
    with open(file_path, 'w') as f:
        f.write(dumps(object, indent=2))