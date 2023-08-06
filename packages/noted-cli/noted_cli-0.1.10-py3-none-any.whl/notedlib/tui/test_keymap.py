import unittest

from notedlib.tui.modes.mode_base import Mode, Action

from .keymap import get_keystroke_action


class TestKeymap(unittest.TestCase):
    def test_should_get_action_from_mode_and_keystroke(self):
        assert get_keystroke_action(Mode.NORMAL, 'q') == Action.QUIT

    def test_should_get_unmapped_action_from_key_not_in_map(self):
        assert get_keystroke_action(Mode.NORMAL, 'z') == Action.UNMAPPED


if __name__ == '__main__':
    unittest.main()
