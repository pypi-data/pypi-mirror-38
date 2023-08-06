import os
import curses
from notedlib.logging import logging


logger = logging.getLogger(__name__)


# TODO: We need something more stable
SPECIAL_KEYS = {
    10: '<Enter>',
    127: '<Backspace>',
    263: '<Backspace>',
    27: '<Escape>',
    9: '<Tab>',
    curses.KEY_RESIZE: '<Resize>',
}


def get_escape_delay():
    os.environ.get('ESCDELAY', 0)


def set_escape_delay(delay_ms):
    os.environ.setdefault('ESCDELAY', str(delay_ms))  # Milliseconds


def normalize_keystroke(raw_keystroke):
    is_special_character = isinstance(raw_keystroke, int)

    logger.debug('Raw keystroke input: %s' % raw_keystroke)

    if is_special_character:
        if raw_keystroke in SPECIAL_KEYS:
            return SPECIAL_KEYS[raw_keystroke]

        return '<Unknown>'

    if len(raw_keystroke) == 1:  # Handles cases like enter (\n)
        if ord(raw_keystroke) in SPECIAL_KEYS:
            return SPECIAL_KEYS[ord(raw_keystroke)]

    return raw_keystroke
