# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:54:50 2016

@author: Elayne Ruane
"""

import unittest
from application.linear_model import get_linear_coef

class Testing(unittest.TestCase):
    
    def test_get_linear_coef(self):
        ''' function that tests whether the function returns the expected coefficient'''
        # test inputs
        folder = 'test_data'
        file_1 = 'full_test'
        file_2 = 'survey_data_test'
        
        # test output
        expected_result = 1.0
        actual_result = get_linear_coef(folder, file_1, file_2)
        self.assertEqual(expected_result, actual_result)
        
    def test_get_linear_coef_output(self):
        # test inputs
        folder = 'test_data'
        file_1 = 'full_test'
        file_2 = 'survey_data_test'
        # test output
        output = get_linear_coef(folder, file_1, file_2)
        # compare
        output_type = type(output)
        expected_type = 'float'
        self.assertEqual(output_type, expected_type)
    
    
if __name__ == '__main__':
    unittest.main()