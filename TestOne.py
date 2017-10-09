import sqlite3

connection = sqlite3.connect("example.db")
cursor = connection.cursor()
cursor.execute("select c, count(*) from (select hash_col, count(*) as c from files_tbl group by hash_col order by c) group by c")

print("hi")

for y in cursor.fetchall():
    print(y)


