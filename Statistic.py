import sqlite3
import hashlib
import os
import threading
import datetime
import time

connection = sqlite3.connect('example.db')
cursor = connection.cursor()
cursor.execute("create table if not exists files_tbl (path_col varchar unique, dir_col varchar, hash_col varchar)")
cursor.execute("create table if not exists locations_tbl (location_col varchar unique, scan_date_col datetime)")
cursor.execute("create view if not exists duplicate_view as select hash_col, count(*) as c from files_tbl group by hash_col order by c")
cursor.execute("create view if not exists duplicate_path_view as select f.path_col from files_tbl f, duplicate_view d where f.hash_col=d.hash_col and d.c > 1")
cursor.execute("create table if not exists duplicates_path_tbl as select * from duplicate_path_view")

#cursor.close()


def has_duplicates(path):
    print("select * from duplicates_path_tbl where path_col like '%s%%'" % path)
    cursor.execute("select * from duplicates_path_tbl where path_col like '%s%%'" % path)
    result = cursor.fetchone()
    return result is not None


def is_scanned(path):
    print("select * from files_tbl where path_col like '%s%%'" % path)
    cursor.execute("select * from files_tbl where path_col like '%s%%'" % path)
    result = cursor.fetchone()
    return result is not None



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
    locations.append("E:\\")
    locations.append("F:\\Foto")
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


class Storage:

    connection = sqlite3.connect('example.db', check_same_thread=False)
    cursor = connection.cursor()

    def get_location_scan_date(self, location):
        self.cursor.execute("select * from locations_tbl")
        for d in self.cursor.fetchall():
            print (d)
        self.cursor.execute("select scan_date_col from locations_tbl where location_col = '%s'" % location)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def cleanup_directory_info(self, directory):
        self.cursor.execute("delete from files_tbl where dir_col = '%s'" % directory)

    def store_file_hash(self, root, file, hash):
        try:
            self.cursor.execute("insert into files_tbl(path_col, dir_col, hash_col) values ('%s', '%s', '%s')" % (os.path.join(root, file), root, hash))
        except sqlite3.OperationalError:
            print("Could not insert value for %s" % os.path.join(root, file))
        finally:
            self.connection.commit()

    def update_location_scan_date(self, location, locationScanDate = None):
        if locationScanDate is None:
            self.cursor.execute("insert into locations_tbl (location_col, scan_date_col) values ('%s', '%s')" % (location, datetime.datetime.now()))
        else:
            self.cursor.execute("update locations_tbl set scan_date_col = '%s' where location_col = '%s'" % (datetime.datetime.now(), location))
        self.connection.commit()


# def get_hash(root, file):
#     hash_md5 = hashlib.md5()
#     with open(os.path.join(root, file), "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()

def get_hash(root, file):
    return os.path.getsize(os.path.join(root, file))


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
        try:
            if is_updated_after_scan(directory, scanDate):
                print(directory + " was updated")
                storage.cleanup_directory_info(directory)
                for item in os.listdir(directory):
                    subitem = os.path.join(directory, item)
                    if (os.path.isdir(subitem)):
                        Scanner.scan(subitem, scanDate, storage)
                    else:
                        try:
                            hash = get_hash(directory, item)
                            storage.store_file_hash(directory, subitem, hash)
                        except FileNotFoundError:
                            print ("File not found %s " % subitem)
            else:
                for item in os.listdir(directory):
                    subitem = os.path.join(directory, item)
                    if (os.path.isdir(subitem)):
                        Scanner.scan(subitem, scanDate, storage)
        except PermissionError:
            print("Permission error reading " + directory)
        except:
            print("Error reading " + directory)

