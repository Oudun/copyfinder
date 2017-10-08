import sqlite3

connection = sqlite3.connect("example.db")
cursor = connection.cursor()
cursor.execute("select * from files_tbl")
for record in cursor.fetchall():
    print(record)
