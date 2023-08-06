from enum import Enum
from notedlib.tui.render_helper import \
    get_win_size, \
    safe_addstr, \
    set_win_background, \
    Point

from notedlib.logging import logging


logger = logging.getLogger(__name__)


class Align(Enum):
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'


class BaseComponent:
    def __init__(self, win, state):
        self.win = win
        self.state = state
        (width, height) = get_win_size(win)
        self.width = width
        self.height = height

    def write_text(self, starting_point: Point, text, **kwargs):
        text_starting_column = starting_point.x

        if kwargs.get('align'):
            text_starting_column = self._get_aligned_text_starting_column(
                    text, kwargs.get('align'))

        safe_addstr(self.win, starting_point.y, text_starting_column, text,
                    kwargs.get('style', 0))

    def _get_aligned_text_starting_column(self, text, align):
        if align == Align.LEFT:
            return 0
        elif align == Align.CENTER:
            return int((self.width / 2) - (len(text) / 2))
        elif align == Align.RIGHT:
            return self.width - len(text) - 1

    def set_background_color(self, color):
        set_win_background(self.win, color)

    def render(self):
        raise NotImplementedError('Not implemented')
