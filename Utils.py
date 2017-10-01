import string
from ctypes import windll


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


if __name__ == '__main__':
    print (get_drives())     # On my PC, this prints ['A', 'C', 'D', 'F', 'H']

def get_parent_path(path):
    index = path.rfind('\\')
    if (index != -1):
        return path[0:path.rfind('\\')+1]
    else:
        print (path)
        return path


