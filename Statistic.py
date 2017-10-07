import sqlite3
import time
from os import walk
import hashlib
import os
import threading
import datetime

connection = sqlite3.connect('example.db')
cursor = connection.cursor()
#cursor.execute("drop table if exists files_tbl")
cursor.execute("create table if not exists files_tbl (path_col varchar unique, dir_col varchar, hash_col varchar)")
cursor.execute("create table if not exists locations_tbl (location_col varchar unique, scan_date_col datetime)")

#is_scanning_now = False

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
    locations.append("D:\\PROJECTS\\copyfinder\\test")
    return locations


def is_updated_after_scan(self, root, directory, locationScanDate = None):
    if locationScanDate is None:
        print("No record for location ")
        return True
    else:
        lastAccessTime = os.path.getatime(os.path.join(root, directory))
        print(lastAccessTime +" > " +  locationScanDate + "=" + (lastAccessTime > locationScanDate))
        return lastAccessTime > locationScanDate
        #return True


class Storage:

    def get_location_scan_date(self, location):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        cursor.execute("select scan_date_col from locations_tbl where location_col = '%s'" % location)
        return cursor.fetchone()

    def cleanup_directory_info(self, directory):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        cursor.execute("delete from files_tbl where dir_col = '%s'" % directory)

    def store_file_hash(self, root, file, hash):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        cursor.execute("insert into files_tbl(path_col, dir_col, hash_col) values ('%s', '%s', '%s')" % (os.path.join(root, file), root, hash))

    def update_location_scan_date(self, location, locationScanDate = None):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        if locationScanDate is None:
            cursor.execute("insert into locations_tbl values ('%s', '%s')" % (location, datetime.datetime.now()))
        else:
            cursor.execute("update locations_tbl set scan_date_col = '%s' where location_col = '%s'" % (datetime.datetime.now(), location))
        print("storing location date " + location)


def get_hash(root, file):
    hash_md5 = hashlib.md5()
    with open(os.path.join(root, file), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class Scanner(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        storage = Storage()
        print('Scanning started')
        for location in get_locations():
            locationScanDate = storage.get_location_scan_date(location)
            for root, directories, files in walk(location):
                try:
                    for directory in directories:
                        try:
                            print("entering %s" % os.path.join(root, directory))
                            if is_updated_after_scan(root, directory, locationScanDate):
                                storage.cleanup_directory_info(root)
                                for file in files:
                                    print("file %s" % os.path.join(root, file))
                                    try:
                                        hash = get_hash(root, file)
                                        storage.store_file_hash(root, file, hash)
                                    except:
                                        print ("failed to parse %s %s" % (root, file))
                            else:
                                print ("No updates")
                        except:
                            print("bad directory %s %s" % (root, directory))
                except:
                    print("something is wrong")
            storage.update_location_scan_date(location, locationScanDate)
                            
                            
