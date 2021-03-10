import unittest
from website.tools import *


class TestTools(unittest.TestCase):

    def test_build_team_view(self):
        test_df_team = pd.read_csv("test_comps")
        test_df_char = pd.read_csv("test_char")
        name_1, html_1 = build_team_view(1, test_df_team, test_df_char)
        self.assertEqual(name_1, "Chosen Brawlers")
        self.assertIn("Hand of Justice", html_1)
        self.assertIn("Chogath", html_1)

    def test_team_len(self):
        test_lst = [0, 1, 2, 3, 4]
        test_df = pd.DataFrame(test_lst)
        result = team_len(test_df)
        self.assertEqual(result, 5)
