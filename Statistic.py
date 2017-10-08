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
    locations.append("D:\\PROJECTS\\copyfinder\\test\\dir1")
    return locations

def is_updated_after_scan(self, fullpath, locationScanDate):
    print("self = " + self)
    print("is_updated_after_scan(%s, %s, %s)" % (self, fullpath, locationScanDate))
    if locationScanDate is None:
        print("No record for location ")
        return True
    else:
        lastAccessTime = os.path.getatime(fullpath)
        print(lastAccessTime +" > " +  locationScanDate + "=" + (lastAccessTime > locationScanDate))
        return lastAccessTime > locationScanDate
        #return True


def is_updated_after_scan_1(self, root, directory, locationScanDate = None):
    print("is_updated_after_scan1(%s, %s, %s, %s)" % self, root, directory, locationScanDate)
    return os.path.getatime(self, os.path.join(root, directory), locationScanDate)






class Storage:

    def get_location_scan_date(self, location):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        cursor.execute("select * from locations_tbl")
        for y in cursor.fetchall():
            print (y)

        print("select scan_date_col from locations_tbl where location_col = '%s'" % location)
        cursor.execute("select scan_date_col from locations_tbl where location_col = '%s'" % location)
        for y in cursor.fetchall():
            print (y)

        cursor.execute("select scan_date_col from locations_tbl where location_col = '%s'" % location)
        print("cursor.fetchone() = " + cursor.fetchone()[0])
#        result = cursor.fetchone()[0]
        result = datetime.datetime.now()
        return result

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
            print("insert into locations_tbl (location_col, scan_date_col) values ('%s', '%s')" % (location, datetime.datetime.now()))
            cursor.execute("insert into locations_tbl (location_col, scan_date_col) values ('%s', '%s')" % (location, datetime.datetime.now()))
            cursor.execute("select * from locations_tbl")
            for y in cursor.fetchall():
                print (y)
            connection.commit()
        else:
            cursor.execute("update locations_tbl set scan_date_col = '%s' where location_col = '%s'" % (datetime.datetime.now(), location))
            cursor.execute("select * from locations_tbl")
            for y in cursor.fetchall():
                print (y)
            connection.commit()
        print("storing location %s date %s " % (location, datetime.datetime.now()))


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
            Scanner.scan(location, locationScanDate, storage)
            storage.update_location_scan_date(location, locationScanDate)

    def scan(directory, scanDate, storage):
        print ("scanning " + directory)
        try:
            if is_updated_after_scan(directory, scanDate):
                storage.cleanup_directory_info(directory)
                for item in os.listdir(directory):
                    subitem = os.path.join(directory, item)
                    if (os.path.isdir(subitem)):
                        Scanner.scan(subitem, scanDate, storage)
                    else:
                        hash = get_hash(directory, item)
                        storage.store_file_hash(directory, subitem, hash);
            else:
                for item in os.listdir(directory):
                    subitem = os.path.join(directory, item)
                    if (os.path.isdir(subitem)):
                        Scanner.scan(subitem, scanDate, storage)
        except PermissionError:
            print("Permission error reading " + directory)
                            
