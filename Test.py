import sqlite3
import time
import datetime
import os
from os import walk

for root, directories, files in walk("D:\\_CACHE"):
    for directory in directories:
        print (os.path.join(root, directory))
        for file in files:
            print (os.path.join(root, file))



# connection = sqlite3.connect('example.db')
# cursor = connection.cursor()
# cursor.execute("select path_col, count(*) as c from files_tbl group by path_col order by c")
# for y in cursor.fetchall():
#     print (y)

# start = datetime.datetime.now()
# for (dirpath, dirnames, filenames) in walk("\\\\wwl-n13\E"):
#     for dirname in (dirnames):
#         try:
#             atime = os.path.getatime(os.path.join(dirpath, dirname))
#             if start- datetime.timedelta(days=365)< datetime.datetime.fromtimestamp(atime):
#                 print (os.path.join(dirpath, dirname)
#                        + " changed " + time.ctime(os.path.getctime(os.path.join(dirpath, dirname)))
#                        + " modified " + time.ctime(os.path.getmtime(os.path.join(dirpath, dirname)))
#                        + " accessed " + time.ctime(os.path.getatime(os.path.join(dirpath, dirname))))
#         except IOError:
#             print ("something wrong with " + dirname)
# print (start)
# print (datetime.datetime.now())

#\\wwl-n13\D
#\\wwl-n13\E
