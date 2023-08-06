from enum import Enum
from notedlib.logging import logging

logger = logging.getLogger(__name__)


class SystemMessage(Enum):
    RERENDER = 'RERENDER'


class Mode(Enum):
    GLOBAL = 'GLOBAL'
    NORMAL = 'NORMAL'
    SEARCH = 'SEARCH'
    TAG = 'TAG'
    ADD_TAG = 'ADD_TAG'
    CONFIRM_DELETE_NOTE = 'CONFIRM_DELETE_NOTE'
    QUIT = 'QUIT'


class Action(Enum):
    QUIT = 'QUIT'
    ERASE = 'ERASE'
    ENTER_SEARCH_MODE = 'ENTER_SEARCH_MODE'
    ENTER_TAG_MODE = 'ENTER_TAG_MODE'
    ENTER_CONFIRM_DELETE_NOTE_MODE = 'ENTER_CONFIRM_DELETE_NOTE_MODE'
    TOGGLE_ORDER_DIRECTION = 'TOGGLE_ORDER_DIRECTION'
    CYCLE_ORDER_BY_VALUE = 'CYCLE_ORDER_BY_VALUE'
    EDIT_SELECTED_NOTE = 'EDIT_SELECTED_NOTE'
    EDIT_NEW_NOTE = 'EDIT_NEW_NOTE'
    ENTER_NORMAL_MODE = 'ENTER_NORMAL_MODE'
    ENTER_ADD_TAG_MODE = 'ENTER_ADD_TAG_MODE'
    SELECT_NEXT_TAG = 'SELECT_NEXT_TAG'
    SELECT_PREV_TAG = 'SELECT_PREV_TAG'
    SELECT_NEXT_NOTE = 'SELECT_NEXT_NOTE'
    SELECT_PREV_NOTE = 'SELECT_PREV_NOTE'
    SELECT_FIRST_NOTE = 'SELECT_FIRST_NOTE'
    SELECT_LAST_NOTE = 'SELECT_LAST_NOTE'
    DELETE_SELECTED_TAG_ON_SELECTED_NOTE = \
        'DELETE_SELECTED_TAG_ON_SELECTED_NOTE'
    CONFIRM_DELETE = 'CONFIRM_DELETE'
    COMMIT = 'COMMIT'
    AUTO_COMPLETE = 'AUTO_COMPLETE'

    RERENDER = 'RERENDER'
    SET_CURSES_OPTk = 'SET_CURSES_OPTS'  # really?
    UNMAPPED = 'UNMAPPED'


class ModeBase:
    def __init__(self, state_container, api):
        self.state_container = state_container
        self.api = api

    def get_action_map(self):
        raise NotImplementedError('A mode must define an action map')

    def handle_keystroke(self, action: Action, keystroke):
        handler_action_map = self.get_action_map()

        if action in handler_action_map:
            logger.debug('Handle keystroke: %s %s' % (keystroke, str(action)))

            if action == Action.UNMAPPED:
                handler_action_map[action](keystroke)
            else:
                handler_action_map[action]()
