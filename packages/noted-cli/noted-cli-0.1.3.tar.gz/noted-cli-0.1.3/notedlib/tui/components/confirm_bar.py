from .base import BaseComponent

from notedlib.tui.render_helper import confirm, Point
from notedlib.tui.modes.mode_base import Mode


class ConfirmBarComponent(BaseComponent):
    def render(self):
        if self.state.get('mode') == Mode.CONFIRM_DELETE_NOTE:
            confirm(self.win, Point(0, 0), 'Are you sure?', ['y', 'n'])
