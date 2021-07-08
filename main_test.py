from main import app
import unittest


class MyTest(unittest.TestCase):

    # ensure flask was set up correctly
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    # ensure all pages loaded correctly
    def test_all_pages(self):
        tester = app.test_client(self)
        response1 = tester.get('/standard')
        self.assertEqual(response1.status_code, 200)
        response2 = tester.get('/custom')
        self.assertEqual(response2.status_code, 200)
        response3 = tester.get('/team/3')
        self.assertEqual(response3.status_code, 200)
        response4 = tester.get('/config')
        self.assertEqual(response4.status_code, 200)

    # ensure correct response after item selection
    def test_select(self):
        tester = app.test_client(self)
        response = tester.post('/custom/select_items', data=dict(result=['Chain Vest']), follow_redirects=True)
        self.assertIn(b'Recommended teams', response.data)
        self.assertIn(b'0/0', response.data)


if __name__ == "__main__":
    unittest.main()
