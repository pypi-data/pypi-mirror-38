from notedlib.tui.modes.mode_base import Mode, Action

# TODO: Define a default, unopinionated keymap
KEYMAP_DEFAULT = {
}

# We are not using the Action enum here since this will probably reside in a
# configuration file later on.
KEYMAP_VI = {
    'GLOBAL': {
    },
    'NORMAL': {
        'q': 'QUIT',
        '/': 'ENTER_SEARCH_MODE',
        'l': 'ENTER_TAG_MODE',
        't': 'ENTER_TAG_MODE',
        'A': 'ENTER_ADD_TAG_MODE',
        'd': 'ENTER_CONFIRM_DELETE_NOTE_MODE',
        'o': 'TOGGLE_ORDER_DIRECTION',
        'O': 'CYCLE_ORDER_BY_VALUE',
        '<Enter>': 'EDIT_SELECTED_NOTE',
        'n': 'EDIT_NEW_NOTE',
        'j': 'SELECT_NEXT_NOTE',
        'k': 'SELECT_PREV_NOTE',
        'g': 'SELECT_FIRST_NOTE',
        'G': 'SELECT_LAST_NOTE',
    },
    'SEARCH': {
        '<Escape>': 'ENTER_NORMAL_MODE',
        '<Enter>': 'COMMIT',
        '<Backspace>': 'ERASE',
    },
    'TAG': {
        '<Escape>': 'ENTER_NORMAL_MODE',
        't': 'ENTER_NORMAL_MODE',
        'a': 'ENTER_ADD_TAG_MODE',
        'l': 'SELECT_NEXT_TAG',
        'h': 'SELECT_PREV_TAG',
        'j': 'SELECT_NEXT_NOTE',
        'k': 'SELECT_PREV_NOTE',
        'x': 'DELETE_SELECTED_TAG_ON_SELECTED_NOTE',
        'd': 'DELETE_SELECTED_TAG_ON_SELECTED_NOTE',
    },
    'ADD_TAG': {
        '<Escape>': 'ENTER_TAG_MODE',
        '<Backspace>': 'ERASE',
        '<Enter>': 'COMMIT',
        '<Tab>': 'AUTO_COMPLETE',
    },
    'CONFIRM_DELETE_NOTE': {
        '<Escape>': 'ENTER_NORMAL_MODE',
        'n': 'ENTER_NORMAL_MODE',
        'y': 'CONFIRM_DELETE',
    },
}

KEYMAP = KEYMAP_VI


def get_keystroke_action(mode: Mode, keystroke):
    mode_mapping = _get_mode_bindings(mode)
    action_name = _get_action_name(mode_mapping, keystroke)

    if action_name and action_name in Action.__members__:
        return Action[action_name]

    return Action.UNMAPPED


def _get_mode_bindings(mode: Mode):
    return KEYMAP[str(mode.value)]


def _get_action_name(mode_mapping, keystroke):
    if keystroke not in mode_mapping:
        return None

    return mode_mapping[keystroke]
