from .base import BaseComponent, Align
from notedlib.tui.render_helper import Point
import notedlib.tui.color as color

import curses  # TODO: Abstract this away?


class TitleBarComponent(BaseComponent):
    def render(self):
        mode_text = '%s' % self.state.get('mode').value

        self.write_text(
                Point(0, 0),
                self.state.get('title'),
                style=curses.A_BOLD)
        self.write_text(
                Point(0, 0),
                mode_text,
                align=Align.RIGHT,
                style=color.get(color.WHITE_ON_BLACK) | curses.A_BOLD)
