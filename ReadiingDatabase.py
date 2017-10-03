import sqlite3

dublicates = []
connection = sqlite3.connect('example.db')
cursor = connection.cursor()

cursor.execute("select count(*),path_col from files_tbl group by path_col")
for x in cursor.fetchall():
        print (x)
connection.commit()

