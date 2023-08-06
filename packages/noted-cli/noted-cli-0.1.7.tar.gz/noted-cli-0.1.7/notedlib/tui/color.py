import curses

WHITE_ON_BLACK = 1
WHITE_ON_GREEN = 2
YELLOW_ON_BLACK = 3
GRAY_ON_BLACK = 4
GREEN_ON_BLACK = 5
RED_ON_BLACK = 6
LIGHT_GRAY_ON_BLACK = 7


def get(color):
    return curses.color_pair(color)


def init():
    curses.init_pair(WHITE_ON_BLACK, 15, 0)
    curses.init_pair(WHITE_ON_GREEN, 15, 10)
    curses.init_pair(YELLOW_ON_BLACK, 11, 0)
    curses.init_pair(GRAY_ON_BLACK, 8, 0)
    curses.init_pair(GREEN_ON_BLACK, 10, 0)
    curses.init_pair(RED_ON_BLACK, 9, 0)
    curses.init_pair(LIGHT_GRAY_ON_BLACK, 7, 0)
