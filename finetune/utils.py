import os

def get_unique_filename(file_path):
    """
    Appends a number to the file name if the file already exists.
    I always overwrite the file by accident so this is a safety measure lol
    """
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path
    while os.path.exists(new_file_path):
        new_file_path = f"{base}({counter}){ext}"
        counter += 1
    return new_file_path