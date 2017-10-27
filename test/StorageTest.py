from unittest import *
from Storage import *


class StorageTest(TestCase):

    storage = None
    storage_location = "test.db"

    def setUp(self):
        self.storage = Storage(self.storage_location)
        print("setUp")

    def tearDown(self):
        print("tearDown")
        self.storage.close()
        os.remove(self.storage_location)

    def test_store_file_hash(self):
        self.storage.store_file_hash("/root", "/root/file1", "abcd")
        self.storage.store_file_hash("/root", "/root/file2", "abcd")
        self.storage.store_file_hash("/root", "/root/file3", "abcde")
        print(self.storage.has_duplicates("/root"))
        assert(self.storage.has_duplicates("/root"))

    def test_is_scanned(self):
        self.storage.store_file_hash("/root/subdir/subsubdir", "/root/subdir/subsubdir/file1", "abc")
        self.storage.store_file_hash("/root", "/root/file2", "abcd")
        self.storage.store_file_hash("/root", "/root/file3", "abcde")
        assert(self.storage.is_scanned("/root"))
        assert(self.storage.is_scanned("/root/subdir"))
        assert(self.storage.is_scanned("/root/subdir/subsubdir"))

    def test_update_location_scan_date(self):
        self.storage.update_location_scan_date('/root')
        assert(self.storage.get_location_scan_date('/root') is not None)
        date = datetime.datetime.now()
        self.storage.update_location_scan_date('/root', date)
        assert(self.storage.get_location_scan_date('/root') == date.strftime('%Y-%m-%d %H:%M:%S.%f'))


# def __init__(self, location = None):
# def is_scanned(self, path):
# def get_location_scan_date(self, location):
# def cleanup_directory_info(self, directory):
# def store_file_hash(self, root, file, hash):
# def update_location_scan_date(self, location, location_scan_date = None):
