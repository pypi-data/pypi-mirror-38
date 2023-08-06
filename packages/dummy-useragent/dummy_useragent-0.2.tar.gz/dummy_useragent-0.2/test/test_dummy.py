import unittest
from dummy_useragent import UserAgent


class Test_Dummy(unittest.TestCase):
    def test_random(self):
        r = UserAgent().random()
        print(r)

    def test_chrome(self):
        u = UserAgent()
        u.Chrome.choice()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
