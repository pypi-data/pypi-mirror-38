from .base import BaseComponent, Align
from notedlib.tui.render_helper import scrollable, Point
from notedlib.helper.string import ellipsis
from notedlib.tui.modes.mode_base import Mode
import notedlib.tui.color as color
import notedlib.tui.symbol as symbol

import math
import curses  # TODO: Abstract this away?

MARGIN_BEFORE_TITLE_COL = 3
MARGIN_AFTER_TITLE_COL = 1


class NoteListComponent(BaseComponent):
    def render(self):
        max_notes_in_viewport = self._get_max_notes_in_list()

        selected_note_index = self.state.get('selected_note_index')
        notes = self.state.get('notes')

        (items, selected_index) = scrollable(
                notes,
                selected_note_index,
                max_notes_in_viewport)

        for index, note in enumerate(items):
            self._draw_note_item(index, index == selected_index, note)

    def _get_max_notes_in_list(self):
        return math.floor(self.height / 2)

    def _draw_note_item(self, index, is_selected, note):
        line_offset = index * self._get_note_height()

        first_row = line_offset
        second_row = first_row + 1

        self._draw_brackets(first_row, is_selected)
        self._draw_title_line(first_row, is_selected, note)
        self._draw_tag_line(second_row, note, is_selected)

    def _get_note_height(self):
        return 2

    def _draw_brackets(self, line_offset, is_selected):
        bracket_style = self._get_bracket_style(is_selected)
        self.write_text(
                Point(1, line_offset),
                symbol.ANGLE_TOP,
                style=bracket_style)
        self.write_text(
                Point(1, line_offset + 1),
                symbol.ANGLE_BOT,
                style=bracket_style)

    def _get_bracket_style(self, is_selected):
        return self._get_highlighted_style() if is_selected else \
            self._get_dimmed_style()

    def _draw_title_line(self, line_offset, is_selected, note):
        self.write_text(
            Point(MARGIN_BEFORE_TITLE_COL, line_offset),
            self._get_note_title_text(note),
            style=self._get_title_text_style(is_selected))
        self.write_text(
            Point(self._get_preview_content_starting_width(note), line_offset),
            self._get_note_preview_text(note),
            style=self._get_dimmed_style())

    def _get_note_title_text(self, note):
        return ellipsis(note.title, self._get_title_max_width())

    def _get_note_preview_text(self, note):
        return ellipsis(note.get_content_preview(),
                        self._get_content_preview_max_width(note))

    def _get_title_max_width(self):
        return self.width - MARGIN_BEFORE_TITLE_COL - MARGIN_AFTER_TITLE_COL

    def _get_content_preview_max_width(self, note):
        return self.width - self._get_preview_content_starting_width(note) - 1

    def _get_title_width(self, note):
        return len(note.title)

    def _get_preview_content_starting_width(self, note):
        return max(0, MARGIN_BEFORE_TITLE_COL +
                      self._get_title_width(note) +
                      MARGIN_AFTER_TITLE_COL)

    def _get_title_text_style(self, is_selected):
        initial_style = curses.A_BOLD
        if is_selected:
            return initial_style | color.get(color.GREEN_ON_BLACK)

        return initial_style | color.get(color.WHITE_ON_BLACK)

    def _draw_tag_line(self, line_offset, note, is_note_selected):
        pos = MARGIN_BEFORE_TITLE_COL
        is_tag_mode = self.state.get('mode') == Mode.TAG
        is_add_tag_mode = self.state.get('mode') == Mode.ADD_TAG
        selected_tag_index = self.state.get('selected_tag_index')

        for tag_index, tag in enumerate(note.tags):
            is_tag_selected = is_tag_mode and \
                is_note_selected and \
                tag_index == selected_tag_index and \
                not is_add_tag_mode

            self.write_text(
                Point(pos, line_offset),
                tag.name,
                style=self._get_tag_text_style(is_tag_mode, is_tag_selected))

            pos += len(tag.name) + 1

        if is_add_tag_mode and is_note_selected:
            self.write_text(
                Point(pos, line_offset),
                ellipsis(self.state.get('new_tag_input_hint'), 40),
                style=self._get_dimmed_style())

            self.write_text(
                Point(pos, line_offset),
                ellipsis(self.state.get('new_tag_input'), 40),
                style=self._get_highlighted_style())

        self._draw_note_date(line_offset, note)

    def _get_tag_text_style(self, is_tag_mode, is_tag_selected):
        if is_tag_selected:
            return self._get_highlighted_style()
        elif is_tag_mode:
            return self._get_semi_dimmed_style()
        else:
            return self._get_dimmed_style()

    def _draw_note_date(self, line_offset, note):
        time_text = ' ↻ %s' % note.updated_at.strftime('%Y-%m-%d %H:%M')
        self.write_text(
            Point(0, line_offset),
            time_text,
            align=Align.RIGHT,
            style=self._get_dimmed_style())

    def _get_dimmed_style(self):
        return color.get(color.GRAY_ON_BLACK)

    def _get_semi_dimmed_style(self):
        return color.get(color.LIGHT_GRAY_ON_BLACK)

    def _get_highlighted_style(self):
        return color.get(color.GREEN_ON_BLACK) | curses.A_BOLD
