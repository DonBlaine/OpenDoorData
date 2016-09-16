import unittest
import pandas as pd

import calendar
import time

from application.model_functions import *

class Testing(unittest.TestCase):

    def test_isempty(self):
        df1 = pd.DataFrame()
        self.assertTrue(isempty_df(df1))
        df2 = pd.DataFrame([[0,'abcd',0,1,123]],columns=['a','b','c','d','e'])
        self.assertFalse(isempty_df(df2))

    def test_convert_to_epoch(self):
        #TODO: REVIEW FUNCTION
        pass
        # df1 = pd.DataFrame([["Wednesday, 27-Jul-16 11:37:51 UTC"]],columns=['time'])
        # df1 = convert_to_epoch(df1, "time")
        # df2 = pd.DataFrame([[1469619471]],columns=['time'])
        # self.assertEqual(df1['time'][0], df2['time'][0])

    def room_number(self):
        df1 = pd.DataFrame([['B002']],columns=['room'])
        df2 = pd.DataFrame([['B106']],columns=['room'])
        df3 = pd.DataFrame([['SC208W']],columns=['room'])
        self.assertEqual(df1['room'][0], 2)
        self.assertEqual(df2['room'][0], 106)
        self.assertEqual(df3['room'][0], 208)

    def estimate_occ(self):
        df1 = pd.DataFrame([[2, 0],[3, 0.5],[4, 1]], columns=['room', 'occupancy_rate'])
        df2 = estimate_occ(df1)
        self.assertTrue(df2['est_occupants'][0], 0)
        self.assertTrue(df2['est_occupants'][1], 45)
        self.assertTrue(df2['est_occupants'][2], 220)

    def dataframe_epochtime_to_datetime(self):
        pass

if __name__ == '__main__':
    unittest.main()