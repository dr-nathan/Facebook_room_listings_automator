# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:21:22 2022

@author: nvs690
"""

import unittest

from helper_functions import (
    extract_location,
    extract_size,
    check_tijdelijk,
    cleanup,
    only_girls,
    location_evaluator,
)

postcodes_of_interest = [
    1011,
    1012,
    1013,
    1014,
    1015,
    1016,
    1017,
    1018,
    1019,
    1051,
    1052,
    1053,
    1054,
    1055,
    1056,
    1057,
    1058,
    1059,
    1071,
    1072,
    1073,
    1074,
    1075,
    1076,
    1077,
    1078,
    1079,
    1091,
    1092,
    1093,
    1094,
    1095,
    1096,
    1097,
    1098,
    1099,
]

class TestMethods(unittest.TestCase):

    def test_extract_location(self):
        self.assertTrue(location_evaluator(postcodes_of_interest,1012, ['donarstraat'], []))
        self.assertTrue(location_evaluator(postcodes_of_interest,1012, [], []))
        self.assertTrue(location_evaluator(postcodes_of_interest,1012, ['rwuig'], []))
        self.assertTrue(location_evaluator(postcodes_of_interest,1012, [], []))
        self.assertTrue(location_evaluator(postcodes_of_interest,None, ['donarstraat'], []))
        self.assertTrue(location_evaluator(postcodes_of_interest,None, ['donarstraat', 'spuistraat'], []))
        self.assertTrue(location_evaluator(postcodes_of_interest,None, ['donarstraat', 'spuistraat'], ['oost']))
        self.assertTrue(location_evaluator(postcodes_of_interest,None, [], ['oost']))
        self.assertTrue(location_evaluator(postcodes_of_interest,None, None, ['oost', 'oost']))
        
        self.assertFalse(location_evaluator(postcodes_of_interest,1025523, ['donarstraat'], []))
        self.assertFalse(location_evaluator(postcodes_of_interest,None, [], []))
        self.assertFalse(location_evaluator(postcodes_of_interest,None, ['lrwjgstraat', 'spuistraat'], []))
        self.assertFalse(location_evaluator(postcodes_of_interest,None, [], ['osdorp']))
        

if __name__ == '__main__':
    unittest.main()