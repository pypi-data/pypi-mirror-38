from .base import BaseComponent, Align

import notedlib.tui.color as color
import notedlib.tui.symbol as symbol
from notedlib.tui.render_helper import Point

# Enums
from notedlib.database import OrderDir
from notedlib.repository.note import NoteOrderField
from notedlib.tui.modes.mode_base import Mode

import curses  # TODO: Abstract this away?


class StatusBarComponent(BaseComponent):
    def render(self):
        self.set_background_color(color.get(color.YELLOW_ON_BLACK))

        # Render search query
        is_search_mode = self.state.get('mode') == Mode.SEARCH
        search_term = self.state.get('search_term')
        search_text_style = color.get(color.YELLOW_ON_BLACK)

        if is_search_mode:
            search_text_style = search_text_style | curses.A_BOLD

        if search_term or is_search_mode:
            search_text = '/%s' % search_term
            self.win.addstr(search_text, search_text_style)

        # Render sorting options
        order_by_text = self._map_note_order_field_to_text(
                self.state.get('order_by'))
        order_dir_text = self._map_order_dir_to_symbol(
                self.state.get('order_dir'))
        order_text = '%s %s' % (order_by_text, order_dir_text)

        self.write_text(Point(0, 0), order_text, align=Align.RIGHT)

    def _map_order_dir_to_symbol(self, order_dir: OrderDir):
        if order_dir == OrderDir.ASC:
            return symbol.ARROW_DOWN

        return symbol.ARROW_UP

    def _map_note_order_field_to_text(self, note_order_field: NoteOrderField):
        if note_order_field == NoteOrderField.CREATED:
            return 'Created'
        elif note_order_field == NoteOrderField.UPDATED:
            return 'Updated'
        elif note_order_field == NoteOrderField.TITLE:
            return 'Title'
        elif note_order_field == NoteOrderField.TAGS:
            return 'Tags'
