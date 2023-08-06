import unittest
from template_pypi.example import examplefunc


class Test_Examplefunc(unittest.TestCase):

    def test1(self):
        x = examplefunc(2.0)
        self.assertEquals(x, 4.0)


# run
if __name__ == '__main__':
    unittest.main()
