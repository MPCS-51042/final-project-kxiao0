import unittest
from website.recom import *


class TestRecom(unittest.TestCase):

    def test_recom(self):
        test_df_team = pd.read_csv("test_comps")
        test_df_items = pd.read_csv("test_item")
        result = recommendation([], test_df_team, test_df_items)
        self.assertEqual(result.shape[0], 20)
        self.assertEqual(result.iloc[0,1], "Chosen Duelists")
