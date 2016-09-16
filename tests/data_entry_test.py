# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:18:01 2016

@author: Elayne Ruane
"""


import unittest

from application.data_entry import epochtime
from application.data_entry import parseName
#from application.data_entry import 


class Testing(unittest.TestCase):
    def test_epochtime(self):
        x = 'Mon Nov 02 20:32:06 GMT+00:00 2015'
        expected_result = 1446496326
        actual_result = epochtime(x)
        self.assertEqual(expected_result, actual_result)
    
    def test_parseName(self):
        x = 'Belfield > Computer Science > B-002'
        expected_result_0 = 'computer science'
        expected_result_1 = '2' 
        actual_result = parseName(x)
        self.assertEqual(expected_result_0, actual_result[0])
        self.assertEqual(expected_result_1, actual_result[1])



if __name__ == '__main__':
    unittest.main()