import unittest

from mock.randomdatagenerator import combineListsOfStruct, Result



class TestRandomGenerator(unittest.TestCase):

    def testCombineListOfStruct(self):
        self.assertEqual(combineListsOfStruct([Result([1, 2, 3], [4, 5, 6]), Result(
            [1, 2, 3], [4, 5, 6])], 'x'), [1, 2, 3, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
