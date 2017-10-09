import sqlite3
from Statistic import has_duplicates

connection = sqlite3.connect("example.db")
cursor = connection.cursor()
cursor.execute("select * from duplicate_path_view")

for record in cursor.fetchall():
    print(record)

print(has_duplicates('D:\PROJECTS\copyfinderj'))

#select * from files_tbl where path_col like 'D:\PROJECTS\copyfinder%'
