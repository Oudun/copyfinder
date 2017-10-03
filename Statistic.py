import sqlite3


connection = sqlite3.connect('example.db')
cursor = connection.cursor()


def get_duplicates(path):
    print ("Getting duplicates for " + path)
    duplicates = []
    cursor.execute("select f2.path_col from files_tbl f1, files_tbl f2 where f1.hash_col==f2.hash_col and f1.path_col!=f2.path_col and f1.path_col='"+path+"'")
    for y in cursor.fetchall():
        print (y)
        duplicates.append(y)
    return duplicates


