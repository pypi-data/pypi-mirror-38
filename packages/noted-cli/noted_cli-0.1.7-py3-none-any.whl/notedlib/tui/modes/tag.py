from .mode_base import ModeBase, Mode, Action


class TagModeHandler(ModeBase):
    def get_action_map(self):
        return {
            Action.ENTER_NORMAL_MODE: self.on_enter_normal_mode,
            Action.SELECT_NEXT_TAG: self.on_select_next_tag,
            Action.SELECT_PREV_TAG: self.on_select_prev_tag,
            Action.SELECT_NEXT_NOTE: self.on_select_next_note,
            Action.SELECT_PREV_NOTE: self.on_select_prev_note,
            Action.DELETE_SELECTED_TAG_ON_SELECTED_NOTE:
                self.on_delete_selected_tag_on_selected_note,
            Action.ENTER_ADD_TAG_MODE: self.on_enter_add_tag_mode,
        }

    def on_enter_normal_mode(self):
        self.state_container.change_mode(Mode.NORMAL)

    def on_select_next_tag(self):
        self.state_container.select_next_tag()

    def on_select_prev_tag(self):
        self.state_container.select_prev_tag()

    def on_select_next_note(self):
        self.state_container.select_first_tag()
        self.state_container.select_next_note()

    def on_select_prev_note(self):
        self.state_container.select_first_tag()
        self.state_container.select_prev_note()

    def on_delete_selected_tag_on_selected_note(self):
        self.state_container.untag_selected_note_and_tag()
        self.state_container.refresh_notes_list()
        self.state_container.refresh_tag_list()

    def on_enter_add_tag_mode(self):
        self.state_container.change_mode(Mode.ADD_TAG)
