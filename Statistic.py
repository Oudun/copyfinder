import hashlib
import os
import threading
import datetime
import time
from Storage import *


def is_scanning():
#    global is_scanning_now
#    return is_scanning_now
    return False


def get_duplicates(path):
    duplicates = []
    # cursor.execute("select f2.path_col from files_tbl f1, files_tbl f2 where f1.hash_col==f2.hash_col and f1.path_col==f2.path_col and f1.path_col='"+path+"'")
    # for y in cursor.fetchall():
    #     duplicates.append(y)
    return duplicates


def get_locations():
    # todo
    locations = []
    #locations.append("\\\\wwl-n13\E")
    locations.append("D:\\")
    #locations.append("F:\\Foto")
    #locations.append("F:\\Foto")
    return locations


def is_updated_after_scan(fullpath, locationScanDate = None):
    if locationScanDate is None:
        print("No record for location ")
        return True
    else:
        last_access_timestamp = os.path.getatime(fullpath)
        lastAccessTime = datetime.datetime.fromtimestamp(last_access_timestamp)
        locationScanTime = datetime.datetime.strptime(locationScanDate, '%Y-%m-%d %H:%M:%S.%f')
        return lastAccessTime > locationScanTime





# def get_hash(root, file):
#     hash_md5 = hashlib.md5()
#     with open(os.path.join(root, file), "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()

def get_hash(root, file):
    return os.path.getsize(os.path.join(root, file))


class Scanner(threading.Thread):

    storage = None

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Scanning started')
        self.storage = Storage()
        for location in get_locations():
            location_scan_date = self.storage.get_location_scan_date(location)
            Scanner.scan(self, location, location_scan_date, self.storage)
            print("Scanning done for %s" % location)
            self.storage.update_location_scan_date(location, location_scan_date)

    def scan(self, directory, scan_date, storage):
        try:
            if is_updated_after_scan(directory, scan_date):
                print(directory + " was updated")
                storage.cleanup_directory_info(directory)
                for item in os.listdir(directory):
                    subitem = os.path.join(directory, item)
                    if (os.path.isdir(subitem)):
                        Scanner.scan(self, subitem, scan_date, self.storage)
                    else:
                        try:
                            hash = get_hash(directory, item)
                            storage.store_file_hash(directory, subitem, hash)
                        except FileNotFoundError:
                            print ("File not found %s " % subitem)
            else:
                for item in os.listdir(directory):
                    subitem = os.path.join(directory, item)
                    if os.path.isdir(subitem):
                        Scanner.scan(self, subitem, scan_date, storage)
        except PermissionError:
            print("Permission error reading " + directory)
        except:
            print("Error reading " + directory)

