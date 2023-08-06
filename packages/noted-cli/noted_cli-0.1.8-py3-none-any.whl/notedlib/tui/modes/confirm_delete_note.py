from .mode_base import ModeBase, Mode, Action


class ConfirmDeleteNoteModeHandler(ModeBase):
    def get_action_map(self):
        return {
            Action.CONFIRM_DELETE: self.on_confirm_delete,
            Action.ENTER_NORMAL_MODE: self.on_enter_normal_mode,
        }

    def on_confirm_delete(self):
        self.state_container.delete_selected_note()
        self.state_container.refresh_notes_list()
        self.state_container.select_prev_note()
        self.state_container.change_mode(Mode.NORMAL)

    def on_enter_normal_mode(self):
        self.state_container.change_mode(Mode.NORMAL)
