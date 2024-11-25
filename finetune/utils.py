import os
import json

def get_unique_filename(file_path):
    """
    Appends a number to the file name if the file already exists.
    I always overwrite the file by accident so this is a safety measure lol
    """
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    while os.path.exists(new_file_path):
        new_file_path = f"{base}({counter}){ext}"
        counter += 1
    return new_file_path

def dump_unique_json(data, file_path):
    """
    Dumps json to a file, appending a number to the file name if it already exists.
    """
    new_file_path = get_unique_filename(file_path)
    with open(new_file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {new_file_path}")
    return new_file_path