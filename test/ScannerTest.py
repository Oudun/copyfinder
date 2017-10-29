from unittest import *
from Storage import *
from Statistic import *

class ScannerTest(TestCase):

    scanner = None
    storage = None
    storage_location = 'test.db'
    test_directory = 'test_directory'

    def setUp(self):
        os.remove(self.test_directory)
        self.scanner = Scanner()
        self.storage = Storage(self.storage_location)
        print("setUp")

    def tearDown(self):
        self.storage.close()
        os.remove(self.test_directory)
        os.remove(self.storage_location)
        print("tearDown")

    def test_scan(self):
        directory = 'test_directory'
        os.makedirs(self.test_directory)
        os.makedirs(os.path.join(self.test_directory, 'subdir_one'), True)
        os.makedirs(os.path.join(self.test_directory, 'subdir_two'), True)
        os.makedirs(os.path.join(self.test_directory, 'subdir_three'), True)
        date = datetime.datetime.now()
        self.scanner.scan(directory, self.storage, date)
        print("test")

