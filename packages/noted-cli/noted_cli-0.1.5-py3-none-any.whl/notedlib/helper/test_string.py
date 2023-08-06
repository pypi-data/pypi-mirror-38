import unittest

from .string import ellipsis


class TestStringHelper(unittest.TestCase):
    def test_ellipsis_should_return_requested_length_including_dots(self):
        too_long_string = 'this is a long string'
        chopped_string = ellipsis(too_long_string, 10)
        self.assertEqual(chopped_string, 'this is ..')


if __name__ == '__main__':
    unittest.main()
