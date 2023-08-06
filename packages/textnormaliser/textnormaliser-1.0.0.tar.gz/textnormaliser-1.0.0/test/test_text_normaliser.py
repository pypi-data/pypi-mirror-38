import unittest
import os
import json
import filecmp
from textnormaliser import _run_normaliser
 
class TestTextNormaliser(unittest.TestCase):
 
    def setUp(self):
        self.textDirectory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_text_files')


    def test_basic(self):
        self.check_test_file('basic.txt')


    def check_test_file(self, test_file):
        test_file_name = os.path.join(self.textDirectory, test_file)
        output_file_name = os.path.join(self.textDirectory, test_file + '.test')
        verify_file_name = os.path.join(self.textDirectory, test_file + '.verify')
        _run_normaliser(test_file_name, output_file_name)
        self.assertTrue(filecmp.cmp(output_file_name, verify_file_name))

 
if __name__ == '__main__':
    unittest.main()
