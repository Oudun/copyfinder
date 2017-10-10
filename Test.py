import os
import datetime

start = datetime.datetime.now()
counter = 1
print (start)
for root, directories, files in os.walk ("D:\\"):
    for directory in directories:
        print (os.path.join(root, directory))
        ++counter
print (start)
print (datetime.datetime.now())
print (counter)
