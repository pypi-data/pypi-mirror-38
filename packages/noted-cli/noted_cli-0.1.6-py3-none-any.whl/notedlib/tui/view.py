from .render_helper import get_sub_win, get_win_size, Area, Point

from .components.title_bar import TitleBarComponent
from .components.status_bar import StatusBarComponent
from .components.note_list import NoteListComponent
from .components.confirm_bar import ConfirmBarComponent

from notedlib.logging import logging

logger = logging.getLogger(__name__)


TITLE_BAR_HEIGHT = 1
TITLE_BAR_START_X = 0
TITLE_BAR_START_Y = 0

STATUS_BAR_HEIGHT = 1
STATUS_BAR_START_X = 0
STATUS_BAR_START_Y = TITLE_BAR_START_Y + TITLE_BAR_HEIGHT

NOTE_LIST_START_X = 0
NOTE_LIST_START_Y = STATUS_BAR_START_Y + STATUS_BAR_HEIGHT

CONFIRM_BAR_HEIGHT = 1
CONFIRM_BAR_START_X = 1


class View:
    def __init__(self, main_win, store):
        self.main_win = main_win
        self.store = store
        self.setup_listeners()

    def setup_listeners(self):
        self.store.subscribe(
                ['title', 'mode'],
                self.render_title_bar)
        self.store.subscribe(
                ['mode', 'search_term', 'order_by', 'order_dir'],
                self.render_status_bar)
        self.store.subscribe(
                [
                    'notes',
                    'mode',
                    'selected_tag_index',
                    'selected_note_index',
                    'new_tag_input',
                    'new_tag_input_hint',
                 ],
                self.render_note_list)
        self.store.subscribe(
                ['mode'],
                self.render_confirm_bar)

    def render_title_bar(self, state):
        win = self._get_title_bar_win()
        TitleBarComponent(win, state).render()

    def _get_title_bar_win(self):
        (main_win_width, main_win_height) = get_win_size(self.main_win)
        win_starting_point = Point(TITLE_BAR_START_X, TITLE_BAR_START_Y)
        title_win_area = Area(win_starting_point, main_win_width, TITLE_BAR_HEIGHT)
        return get_sub_win(self.main_win, title_win_area)

    def render_status_bar(self, state):
        win = self._get_status_bar_win()
        StatusBarComponent(win, state).render()

    def _get_status_bar_win(self):
        (main_win_width, _) = get_win_size(self.main_win)
        win_starting_point = Point(STATUS_BAR_START_X, STATUS_BAR_START_Y)
        status_bar_area = Area(win_starting_point, main_win_width, STATUS_BAR_HEIGHT)
        return get_sub_win(self.main_win, status_bar_area)

    def render_note_list(self, state):
        win = self._get_note_list_win()
        NoteListComponent(win, state).render()

    def _get_note_list_win(self):
        (main_win_width, _) = get_win_size(self.main_win)
        win_starting_point = Point(NOTE_LIST_START_X, NOTE_LIST_START_Y)
        note_list_area = Area(win_starting_point,
                              main_win_width,
                              self._get_note_list_height())
        return get_sub_win(self.main_win, note_list_area)

    def _get_note_list_height(self):
        (_, main_win_height) = get_win_size(self.main_win)
        return main_win_height - \
            TITLE_BAR_HEIGHT - \
            STATUS_BAR_HEIGHT - \
            CONFIRM_BAR_HEIGHT

    def render_confirm_bar(self, state):
        win = self._get_confirm_bar_win()
        ConfirmBarComponent(win, state).render()

    def _get_confirm_bar_win(self):
        (main_win_width, main_win_height) = get_win_size(self.main_win)
        win_starting_point = Point(CONFIRM_BAR_START_X, main_win_height - 1)
        confirm_bar_area = Area(win_starting_point,
                                main_win_width - CONFIRM_BAR_START_X,
                                CONFIRM_BAR_HEIGHT)
        return get_sub_win(self.main_win, confirm_bar_area)
