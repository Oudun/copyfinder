import sqlite3
import os
import datetime


class Storage:

    cursor = None
    connection = None

    def __init__(self, location = None):
        if location is None:
            location = 'example.db'
        self.connection = sqlite3.connect(location)
        self.cursor = self.connection.cursor()
        self.cursor.execute("create table if not exists files_tbl (path_col varchar unique, dir_col varchar, hash_col varchar)")
        self.cursor.execute("create table if not exists locations_tbl (location_col varchar unique, scan_date_col datetime)")
        self.cursor.execute("create view if not exists duplicate_view as select hash_col, count(*) as c from files_tbl group by hash_col order by c")
        self.cursor.execute("create view if not exists duplicate_path_view as select f.path_col from files_tbl f, duplicate_view d where f.hash_col=d.hash_col and d.c > 1")
        print("storage created")

    def close(self):
        self.cursor.close()
        self.connection.close()

    def has_duplicates(self, path):
        self.cursor.execute("select * from duplicate_path_view where path_col like '%s%%'" % path)
        result = self.cursor.fetchone()
        return result is not None


    def is_scanned(self, path):
        self.cursor.execute("select * from files_tbl")
        result = self.cursor.fetchone()
        for y in result:
            print(y)
        print("select * from files_tbl where path_col like '%s%%'" % path)
        self.cursor.execute("select * from files_tbl where path_col like '%s%%'" % path)
        result = self.cursor.fetchone()
        return result is not None

    def get_location_scan_date(self, location):
        self.cursor.execute("select * from locations_tbl")
        for d in self.cursor.fetchall():
            print (d)
        self.cursor.execute("select scan_date_col from locations_tbl where location_col = '%s'" % location)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def cleanup_directory_info(self, directory):
        self.cursor.execute("delete from files_tbl where dir_col = '%s'" % directory)

    def store_file_hash(self, root, file, hash):
        try:
            self.cursor.execute("insert into files_tbl(path_col, dir_col, hash_col) values ('%s', '%s', '%s')" % (os.path.join(root, file), root, hash))
        except sqlite3.OperationalError:
            print("Could not insert value for %s" % os.path.join(root, file))
        finally:
            self.connection.commit()

    def update_location_scan_date(self, location, location_scan_date = None):
        if location_scan_date is None:
            self.cursor.execute("insert into locations_tbl (location_col, scan_date_col) values ('%s', '%s')" % (location, datetime.datetime.now()))
        else:
            self.cursor.execute("update locations_tbl set scan_date_col = '%s' where location_col = '%s'" % (datetime.datetime.now(), location))
        self.connection.commit()
