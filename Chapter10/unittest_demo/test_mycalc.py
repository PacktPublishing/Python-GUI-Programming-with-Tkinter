import mycalc
import unittest
from unittest.mock import Mock, patch

class TestMyCalc(unittest.TestCase):

    def setUp(self):
        self.mycalc1_0 = mycalc.MyCalc(1, 0)
        self.mycalc36_12 = mycalc.MyCalc(36, 12)

    def test_add(self):
        self.assertEqual(self.mycalc1_0.add(), 1)
        self.assertEqual(self.mycalc36_12.add(), 48)

    def test_mod_divide(self):
        self.assertEqual(self.mycalc36_12.mod_divide(), (3, 0))
        self.assertRaises(ValueError, self.mycalc1_0.mod_divide)

        with self.assertRaises(ValueError):
            self.mycalc1_0.mod_divide()

    def test_rand_between(self):

        # not a good way to do it:
        rv = self.mycalc1_0.rand_between()
        self.assertLessEqual(rv, 1)
        self.assertGreaterEqual(rv, 0)

        # better, but clumsy
        fakerandom = Mock(return_value=.5)
        orig_random = mycalc.random.random
        mycalc.random.random = fakerandom
        rv = self.mycalc1_0.rand_between()
        self.assertEqual(rv, 0.5)
        mycalc.random.random = orig_random

        # clean and neat
        with patch('mycalc.random.random') as fakerandom:
            fakerandom.return_value = 0.5
            rv = self.mycalc1_0.rand_between()
            self.assertEqual(rv, 0.5)

    @patch('mycalc.random.random')
    def test_rand_between2(self, fakerandom):
        fakerandom.return_value = 0.5
        rv = self.mycalc1_0.rand_between()
        self.assertEqual(rv, 0.5)


if __name__ == '__main__':
    unittest.main()
