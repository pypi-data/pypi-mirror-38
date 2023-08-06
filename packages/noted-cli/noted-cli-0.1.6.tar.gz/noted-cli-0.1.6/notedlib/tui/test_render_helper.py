import unittest
from unittest.mock import Mock, MagicMock

import notedlib.tui.render_helper as render


class TestRenderHelper(unittest.TestCase):

    def setUp(self):
        self.test_items = ['one', 'two', 'three', 'four', 'five']

    def test_scrollable(self):
        """Scrollable should be able to calculate the 'window' of items,
        including the relative index of the selected item."""

        # Make sure that it handles both ends
        (items, selected) = render.scrollable(self.test_items, 0, 3)
        self.assertEqual(items, ['one', 'two', 'three'])
        self.assertEqual(selected, 0)

        (items, selected) = render.scrollable(self.test_items, 1, 3)
        self.assertEqual(items, ['one', 'two', 'three'])
        self.assertEqual(selected, 1)

        (items, selected) = render.scrollable(self.test_items, 2, 3)
        self.assertEqual(items, ['two', 'three', 'four'])
        self.assertEqual(selected, 1)

        (items, selected) = render.scrollable(self.test_items, 3, 3)
        self.assertEqual(items, ['three', 'four', 'five'])
        self.assertEqual(selected, 1)

        (items, selected) = render.scrollable(self.test_items, 4, 3)
        self.assertEqual(items, ['three', 'four', 'five'])
        self.assertEqual(selected, 2)

        # Test with bigger max value than available items
        (items, selected) = render.scrollable(self.test_items, 4, 10)
        self.assertEqual(items, ['one', 'two', 'three', 'four', 'five'])
        self.assertEqual(selected, 4)

    def test_safe_addstr_should_stop_drawing_outside_window(self):
        # Visual represenation of test (x=16)
        # 0                x  20
        # --------------------|
        #                  foo|bar
        #                     |
        mock_win = self._get_mock_win(width=20, height=20)
        render.safe_addstr(mock_win, 0, 16, 'foobar')
        mock_win.addstr.assert_called_with(0, 16, 'foo')

    def test_safe_addstr_should_not_begin_drawing_out_of_bounds(self):
        mock_win = self._get_mock_win(width=20, height=20)
        render.safe_addstr(mock_win, 0, 20, 'foobar')
        render.safe_addstr(mock_win, 20, 0, 'foobar')
        mock_win.addstr.assert_not_called()

    def _get_mock_win(self, **kwargs):
        win = Mock()
        dimensions = (kwargs.get('height', 20), kwargs.get('width', 20))
        win.getmaxyx = MagicMock(return_value=dimensions)
        win.addstr = MagicMock()
        return win


if __name__ == '__main__':
    unittest.main()
