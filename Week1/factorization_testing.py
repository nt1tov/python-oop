# import unittest

# def factorize(x):
#     """ 
#     Factorize positive integer and return its factors.
#     :type x: int,>=0
#     :rtype: tuple[N],N>0
#     """
#     pass


class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        with self.subTest(x=1):
            self. assertRaises (TypeError, factorize, 'string')
        with self.subTest(x=1):
            self. assertRaises (TypeError, factorize, 1.5)

    def test_negative(self):
        cases = [-1, -10, -100]
        for case in cases:
            with self.subTest(x=case):
                self.assertRaises (ValueError, factorize, case)

    def test_zero_and_one_cases(self):
        cases = [ (0, (0,)), (1, (1,)) ]
        for case in cases:
            with self.subTest(x=case[0]):
                self.assertEqual(factorize(case[0]), case[1])

    def test_simple_numbers(self):
       # 3 → (3, ),  13 → (13, ),   29 → (29, )
        cases = [(3, (3,)), (13, (13,)), (29, (29,)) ]
        for case in cases:
            with self.subTest(x=case[0]):
                self.assertEqual(factorize(case[0]), case[1])

    def test_two_simple_multipliers(self):
        # 6 → (2, 3),   26 → (2, 13),   121 --> (11, 11)
        cases = [(6, (2, 3)), (26, (2, 13)), (121, (11, 11)) ]
        for case in cases:
            with self.subTest(x=case[0]):
                self.assertEqual(factorize(case[0]), case[1])

    def test_many_multipliers(self):
        #1001 → (7, 11, 13) ,   9699690 → (2, 3, 5, 7, 11, 13, 17, 19)
        cases = [(1001, (7, 11, 13)), (9699690, (2, 3, 5, 7, 11, 13, 17, 19))]
        for case in cases:
            with self.subTest(x=case[0]):
                self.assertEqual(factorize(case[0]), case[1])