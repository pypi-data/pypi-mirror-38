import unittest
import curses

from .input import normalize_keystroke


class TestInput(unittest.TestCase):
    def test_normalize_keystroke_should_handle_special_keys(self):
        assert normalize_keystroke(10) == '<Enter>'
        assert normalize_keystroke(127) == '<Backspace>'
        assert normalize_keystroke(27) == '<Escape>'
        assert normalize_keystroke(999) == '<Unknown>'
        assert normalize_keystroke(curses.KEY_RESIZE) == '<Resize>'

    def test_normalize_keystroke_should_handle_normal_keys(self):
        assert normalize_keystroke('a') == 'a'
        assert normalize_keystroke('z') == 'z'


if __name__ == '__main__':
    unittest.main()
