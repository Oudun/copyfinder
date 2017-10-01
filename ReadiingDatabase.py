import sqlite3

dublicates = []
connection = sqlite3.connect('example.db')
cursor = connection.cursor()

cursor.execute("select ph, count(*) from ph group by ph")
for x in cursor.fetchall():
    if (x[1]>2):
        dublicates.append(x[0])
        print (x[0])
# prints ('arw', '3367')
connection.commit()

for hash in dublicates:
    print (hash)
    cursor.execute("select * from ph where ph='"+hash+"'")
    for y in cursor.fetchall():
        print (y)

