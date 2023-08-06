from .mode_base import ModeBase, Mode, Action, SystemMessage


class NormalModeHandler(ModeBase):
    def get_action_map(self):
        return {
            Action.QUIT: self.on_quit,
            Action.TOGGLE_ORDER_DIRECTION: self.on_toggle_order_direction,
            Action.CYCLE_ORDER_BY_VALUE: self.on_cycle_order_by_value,
            Action.CYCLE_ORDER_BY_VALUE: self.on_cycle_order_by_value,
            Action.EDIT_SELECTED_NOTE: self.on_edit_selected_note,
            Action.SELECT_NEXT_NOTE: self.on_select_next_note,
            Action.SELECT_PREV_NOTE: self.on_select_prev_note,
            Action.SELECT_FIRST_NOTE: self.on_select_first_note,
            Action.SELECT_LAST_NOTE: self.on_select_last_note,
            Action.ENTER_SEARCH_MODE: self.on_enter_search_mode,
            Action.ENTER_TAG_MODE: self.on_enter_tag_mode,
            Action.ENTER_ADD_TAG_MODE: self.on_enter_add_tag_mode,
            Action.EDIT_NEW_NOTE: self.on_edit_new_note,
            Action.ENTER_CONFIRM_DELETE_NOTE_MODE:
                self.on_enter_confirm_delete_note_mode,
        }

    def on_quit(self):
        self.state_container.change_mode(Mode.QUIT)

    def on_toggle_order_direction(self):
        self.state_container.toggle_order_direction()
        self.state_container.refresh_notes_list()

    def on_cycle_order_by_value(self):
        self.state_container.rotate_order_by_field()
        self.state_container.refresh_notes_list()

    def on_edit_selected_note(self):
        self.state_container.edit_content()
        self.state_container.refresh_notes_list()
        self.state_container.append_system_message(SystemMessage.RERENDER)

    def on_select_next_note(self):
        self.state_container.select_next_note()

    def on_select_prev_note(self):
        self.state_container.select_prev_note()

    def on_select_first_note(self):
        self.state_container.select_first_note()

    def on_select_last_note(self):
        self.state_container.select_last_note()

    def on_enter_search_mode(self):
        self.state_container.change_mode(Mode.SEARCH)

    def on_enter_tag_mode(self):
        self.state_container.change_mode(Mode.TAG)

    def on_enter_add_tag_mode(self):
        self.state_container.change_mode(Mode.ADD_TAG)

    def on_edit_new_note(self):
        self.state_container.create_new_note()
        self.state_container.refresh_notes_list()
        self.state_container.append_system_message(SystemMessage.RERENDER)

    def on_enter_confirm_delete_note_mode(self):
        self.state_container.change_mode(Mode.CONFIRM_DELETE_NOTE)
