import unittest
from ybc_history import *


class MyTestCase(unittest.TestCase):
    def test_history(self):
        content = ['2010年1月1日，中国－东盟自贸区正式建成。', '2006年1月1日，中国政府废止农业税。', '1999年1月1日，欧元诞生。']

        self.assertEqual(content, history_info(1, 1, 3, "list"))


if __name__ == '__main__':
    unittest.main()
