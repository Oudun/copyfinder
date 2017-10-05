import sqlite3
import time
from os import walk
import hashlib
import os
import threading

connection = sqlite3.connect('example.db')
cursor = connection.cursor()
cursor.execute("drop table if exists files_tbl")
cursor.execute("create table if not exists files_tbl (path_col varchar unique, hash_col varchar)")

#is_scanning_now = False

def is_scanning():
#    global is_scanning_now
#    return is_scanning_now
    return False


def get_duplicates(path):
    duplicates = []
    cursor.execute("select f2.path_col from files_tbl f1, files_tbl f2 where f1.hash_col==f2.hash_col and f1.path_col==f2.path_col and f1.path_col='"+path+"'")
    for y in cursor.fetchall():
        duplicates.append(y)
    return duplicates

def get_locations():
    # todo
    locations = []
    #locations.append("\\\\wwl-n13\E")
    locations.append("D:\\")
    return locations


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def scan():
    #global is_scanning_now
    #is_scanning_now = True
    print('Scanning started')
    counter = 0
    for location in get_locations():
        for root, directories, files in walk(location):
            for file in files:
                try:
                    hash = md5(os.path.join(root, file))
                    print (hash + " " + os.path.join(root, file))
                    cursor.execute("insert into files_tbl(path_col, hash_col) values ('" + os.path.join(root, file) + "', '" + hash + "')")
                except :
                    print ("Error to process " + os.path.join(root, file))
                counter +=1
                if (counter%1000==0):
                    connection.commit()
                    print ('records stored: '+ str(counter))
        print (location + "done")

    #is_scanning_now = False


class Scanner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Scanning started')
        counter = 0
        for location in get_locations():
            for root, directories, files in walk(location):
                for file in files:
                    try:
                        hash = md5(os.path.join(root, file))
                        print (hash + " " + os.path.join(root, file))
                        cursor.execute("insert into files_tbl(path_col, hash_col) values ('" + os.path.join(root, file) + "', '" + hash + "')")
                    except :
                        print ("Error to process " + os.path.join(root, file))
                    counter +=1
                    if (counter%1000==0):
                        connection.commit()
                        print ('records stored: '+ str(counter))
            print (location + "done")
