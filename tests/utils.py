import os
import unittest

import sys
sys.path.insert(0, '..')

class TemplarTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def open_data(filename):
        path = os.path.join(os.path.dirname(__file__), 'test-data')
        if not os.path.exists(os.path.join(path, filename)):
            print('No file', filename, 'found in', path)
        with open(os.path.join(path, filename), 'r') as f:
            return f.read()

def main():
    unittest.main()
