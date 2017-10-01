import dbm
import sqlite3
#import gadfly
import hashlib
from os import walk

connection = sqlite3.connect('example.db')
cursor = connection.cursor()
cursor.execute("create table if not exists ph (nm varchar, ph varchar)")


#connection = gadfly.gadfly()
#connection.startup("mydatabase", "/home")
#cursor = connection.cursor()
#cursor.execute("create table ph (nm varchar, ph varchar)")


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


fullPath = ''
fullPathEscaped = ''
counter=0
for (dirpath, dirnames, filenames) in walk("D:\\MinecraftSaves"):
    for file in (filenames):
        fullPath = dirpath+"\\"+file
        fullPathEscaped = dirpath.replace('\'','').replace('\"','\\\"').replace('`','')+"\\" + file.replace('\'','').replace('\"','\\\"').replace('`','')
        try:
            print (md5(fullPath)+" "+fullPath)
            cursor.execute("insert into ph(nm, ph) values ('" + fullPathEscaped+ "', '" + md5(dirpath+"\\"+file) + "')")
        except IOError:
            print ("IOError to process " + fullPath)
        counter +=1
        if (counter%1000==0):
            connection.commit()
            print ('records stored: '+ str(counter))

cursor.execute("select * from ph")
for x in cursor.fetchall():
  print (x)
# prints ('arw', '3367')
connection.commit()


