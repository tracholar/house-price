import unittest
import scraw

class TestBase(unittest.TestCase):
    def test_hello(self):
        self.assertEqual("hello", "hello")

class TestScraw(unittest.TestCase):
    def test_get_dom_from_string(self):
        dom = scraw.get_dom_from_string('''
        <html>
            <body>
                <p>Hello word</p>
            </body>
        </html>
        ''')
        self.assertIsNotNone(dom)



if __name__ == '__main__':
    unittest.main()