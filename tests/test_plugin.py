import unittest

class SalomeKratosPlugin(unittest.TestCase):

    def test_working_test_case(self):
        self.assertEqual(1,1)
        self.assertTrue(True)

    def test_failing_test_case(self):
        self.assertFalse(True)



if __name__ == '__main__':
    unittest.main()
