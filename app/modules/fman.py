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
    with open(path, 'a+') as f:
        # If the last character is not a newline, add a newline before writing
        if f.tell() > 0:  # Check if the file is not empty
            f.seek(f.tell() - 1) # Move the cursor back one character
            last_char = f.read()
            if last_char != '\n':
                f.write('\n')
        f.write(f'{field}={value}')


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


class arch:
    """
    # This class is used to initialize an archive object for file management.
    # It will be rewritten in the future.
    """
    def __init__(self, name: str, format: str = 'zip') -> None:
        self.name = name
        self.format = format.lower()
        if self.format not in ['zip', 'xztar', 'bztar', 'tar', 'gztar']:
            raise ValueError("Unsupported archive format. Use 'zip', 'xztar', 'bztar', 'tar', 'gztar'.")

    def compress(self, root: str) -> None:
        """
        # This method creates an archive of root folder with the specified format.
        """
        from shutil import make_archive
        return make_archive(self.name, self.format, root)
