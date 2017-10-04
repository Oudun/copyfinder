import sqlite3
import time

connection = sqlite3.connect('example.db')
cursor = connection.cursor()
is_scanning_now = False


def is_scanning():
    global is_scanning_now
    return is_scanning_now


def get_duplicates(path):
    print ("Getting duplicates for " + path)
    duplicates = []

    cursor.execute("select * from files_tbl where hash_col='78ee691dabb5a26686134c34edfb220d'")
    for y in cursor.fetchall():
        print(y)
        print('sssssssssssssssssss')
#        filehash = y
#        print('filehash ' + filehash[0])

    return

    print('should not see me')

    cursor.execute("select hash_col from files_tbl where path_col='"+path+"'")
    for y in cursor.fetchall():
        filehash = y
        print('filehash ' + filehash[0])

    cursor.execute("select path_col from files_tbl where hash_col='"+filehash[0]+"'")
    for y in cursor.fetchall():
        print(y)
#        duplicates.append[y[0]]



    #cursor.execute("select f2.path_col from files_tbl f1, files_tbl f2 where f1.hash_col==f2.hash_col and f1.path_col==f2.path_col and f1.path_col='"+path+"'")
    #for y in cursor.fetchall():
    #    print (y)
    #    duplicates.append(y)


#get_duplicates("D:\\PYTHON_PROJECTS\\copyfinder\\test\\trixer")

cursor.execute("select * from files_tbl")
for y in cursor.fetchall():
    print(y)


def scan():
    global is_scanning_now
    is_scanning_now = True
    time.sleep(10000)
    is_scanning_now = False

