import math
import curses

import notedlib.tui.color as color

from notedlib.logging import logging

from collections import namedtuple

logger = logging.getLogger(__name__)


Point = namedtuple('Point', 'x y')


class Area:
    def __init__(self, starting_point: Point, width: int, height: int):
        self.starting_point = starting_point
        self.width = width
        self.height = height

    def __repr__(self):
        return '<Area starting_point=%s width=%s height=%s>' % (
                str(self.starting_point),
                self.width, self.height)


def get_sub_win(parent_win, area: Area):
    if area.width and area.height:
        sub_win = parent_win.derwin(area.height, area.width,
                                    area.starting_point.y,
                                    area.starting_point.x)
    else:
        sub_win = parent_win.derwin(
            area.starting_point.y,
            area.starting_point.x)

    sub_win.clear()
    return sub_win


def get_win_size(win):
    (y, x) = win.getmaxyx()
    return (x, y)


def safe_addstr(win, *args, **kwargs):
    """Wraps addstr and makes sure that we don't draw outside the window"""
    (max_x, max_y) = get_win_size(win)
    args = list(args)
    (y, x) = args[0:2]

    if isinstance(x, int) and isinstance(y, int):
        if y >= max_y or y < 0 or x >= max_x or x < 0:
            return

    requested_text = args[2]
    remaining_line_width = max_x - x - 1
    args[2] = requested_text[0:min(remaining_line_width, len(requested_text))]

    try:
        win.addstr(*tuple(args))
    except Exception as e:
        logger.error('Failed to write text to window: %s' % str(e))


def set_win_background(win, color):
    win.bkgd(' ', color)


def confirm(win, position: Point, msg, options=[], severity='danger'):
    text_style = color.get(color.RED_ON_BLACK) | curses.A_BOLD
    text = '%s (%s)' % (msg, '/'.join(options))
    safe_addstr(win, position.y, position.x, text, text_style)


def scrollable(items, selected_index, max_items):
    # Keep middle above middle if not even (wut?)
    middle = math.floor(max_items / 2)
    start = min(max(0, selected_index - middle), max(0, len(items) -
                                                     max_items))
    end = min(len(items), start + max_items)

    result_items = items[start:end]
    cursor = 0

    # TODO: Looking up the index by value is so stupid
    for index, item in enumerate(result_items):
        if len(items) > selected_index and items[selected_index] == item:
            cursor = index
            break

    return (result_items, cursor)
