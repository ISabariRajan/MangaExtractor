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
    
    """
    The download_file function downloads a file from the internet and saves it to disk.
        Args:
            url (str): The URL of the file to download.
            filename (str): The name of the local file where you want to save it.
    
    :param url: Specify the url to download from
    :param filename: Specify the name of the file to be downloaded
    :return: A file object
    :doc-author: Sabari
    """
    data = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(data)    

def non_char_to_underscore(text):
    
    """
    The non_char_to_underscore function takes a string as input and returns the same string with all non-alphanumeric characters replaced by underscores.
    
    :param text: Pass in the text that needs to be checked
    :return: A string with all non-alphanumeric characters replaced by underscores
    :doc-author: Sabari
    """
    check_text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY1234567890.-"
    text = text.strip()
    new_text = ""
    for t in text:
        if t in check_text:
            new_text += t
        else:
            new_text += "_"
    
    return new_text

def create_new_folder(folder_name):
    
    """
    The create_new_folder function creates a new folder if it does not already exist.
        Args:
            folder_name (str): The name of the folder to be created.
        Returns: 
            str: The name of the newly created or existing folder.
    
    :param folder_name: Create a new folder with the name of the parameter
    :return: The folder name
    :doc-author: Sabari
    """
    if not file_exists(folder_name):
        makedirs(folder_name)
    return folder_name

def read_json(file_path):
    
    """
    The read_json function reads a JSON file and returns the contents as a Python dictionary.
        
        Args:
            file_path (str): The path to the JSON file to be read.
    
    :param file_path: Specify the path to the file that is being read
    :return: A dictionary of the json file
    :doc-author: Sabari
    """
    output = None
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if lines:
            output = loads("".join(lines))
    return output

def write_json(file_path, object):
    
    """
    The write_json function takes a file path and an object as arguments.
    It then writes the object to the specified file in JSON format.
    
    :param file_path: Specify the path of the file to be written
    :param object: Write the object to a file
    :return: A string
    :doc-author: Sabari
    """
    with open(file_path, 'w') as f:
        f.write(dumps(object, indent=2))