import curses

from notedlib.noted import API

import notedlib.tui.input as input
import notedlib.tui.keymap as keymap
import notedlib.tui.editor as editor

# Enums
from notedlib.tui.modes.mode_base import Mode, SystemMessage
from notedlib.database import OrderDir
from notedlib.repository.note import NoteOrderField

from notedlib.tui.modes.normal import NormalModeHandler
from notedlib.tui.modes.search import SearchModeHandler
from notedlib.tui.modes.tag import TagModeHandler
from notedlib.tui.modes.add_tag import AddTagModeHandler
from notedlib.tui.modes.confirm_delete_note import ConfirmDeleteNoteModeHandler

from notedlib.subscribable_dict import SubscribableDict
from notedlib.tui.state_container import StateContainer

from notedlib.tui.view import View
import notedlib.tui.color as color


def get_initial_state():
    return {
        'title': 'NOTED',
        'mode': Mode.NORMAL,
        'key_input': '',
        'order_by': NoteOrderField.UPDATED,
        'order_dir': OrderDir.DESC,
        'search_term': '',
        'key': ' ',
        'notes': [],
        'tags': [],
        'selected_note_index': 0,
        'selected_note_id': None,
        'selected_tag_index': 0,
        'new_tag_input': '',
        'new_tag_input_hint': '',
        'system_msq': [],
    }


class TUIApp:
    def __init__(self, api: API):
        self.state = SubscribableDict(get_initial_state())
        self.state_container = StateContainer(api, self.state, editor)
        self.main_win = None
        self.view = None
        self.mode_handlers = {
            Mode.NORMAL: NormalModeHandler(self.state_container, api),
            Mode.SEARCH: SearchModeHandler(self.state_container, api),
            Mode.TAG: TagModeHandler(self.state_container, api),
            Mode.ADD_TAG: AddTagModeHandler(self.state_container, api),
            Mode.CONFIRM_DELETE_NOTE: ConfirmDeleteNoteModeHandler(
                self.state_container, api),
        }

    def _setup_curses(self):
        curses.cbreak()        # Character break mode
        curses.curs_set(0)     # Hide the cursor
        curses.noecho()        # Do not output chars as we type
        color.init()           # Initialize color pairs

    def _clear_screen(self):
        self.main_win.clear()

    def _force_render(self):
        self.state.emit_all_subscribers()

    def _connect_store_to_view(self):
        self.view = View(self.main_win, self.state)
        self.state.subscribe([], self._on_state_change)

    def _on_state_change(self, state):
        self.render(state)

    def render(self, state):
        # TODO: Place this inside view class?
        self.main_win.noutrefresh()
        curses.doupdate()

    def main(self, stdscr):
        self.main_win = stdscr
        self.main_win.keypad(True)

        self._clear_screen()
        self._setup_curses()
        self._connect_store_to_view()
        self._force_render()

        # Load initial list of notes
        self.state_container.refresh_notes_list()

        # Load all existing tags for quick access
        self.state_container.refresh_tag_list()

        current_mode = self.state.get('mode')

        while current_mode != Mode.QUIT:
            raw_keystroke = self.main_win.get_wch()
            keystroke = input.normalize_keystroke(raw_keystroke)

            action = keymap.get_keystroke_action(current_mode, keystroke)
            self.mode_handlers[current_mode].handle_keystroke(
                action, keystroke)

            self._global_key_handler(keystroke)

            current_mode = self.state.get('mode')
            self._handle_system_msq(self.state.get('system_msq', []))

    def _global_key_handler(self, keystroke):
        if keystroke == '<Resize>':
            self._force_rerender()

    def _force_rerender(self):
        self._clear_screen()
        self._force_render()

    # TODO: This is dirty
    def _handle_system_msq(self, queue):
        while len(queue):
            msg = queue.pop()

            if msg == SystemMessage.RERENDER:
                self._force_rerender()
