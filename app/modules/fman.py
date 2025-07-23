from os import remove, rmdir, listdir
from os.path import exists, isdir, join

def env_read(path : str, field : str) -> str | None:
    """
    # This function searches for a file (.env) and read the value from a specified field.
    # It returns the value of the field if it exists, or None if it does not.
    """
    if exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.startswith(f'{field}='):
                    return line.strip().split('=', 1)[1] # Splits the line at the first '=' once and returns the second part (the value)
    else:
        return None


def env_write(path : str, field : str, value : str) -> None:
    """
    # This function writes a value to a specified field in a file (.env).
    """
    with open(path, 'a') as f:
        f.write(f'{field}={value}\n')


def rmrf(path : str) -> None:
    """
    # This function deletes a file or directory recursively.
    """
    if exists(path):
        if isdir(path):
            for item in listdir(path):
                rmrf(join(path, item))  # Recursively remove items in the directory
            rmdir(path)  # Remove the empty directory
        else:
            remove(path)  # Remove the file
