from .mode_base import ModeBase, Mode, Action


class AddTagModeHandler(ModeBase):
    def get_action_map(self):
        return {
            Action.ENTER_TAG_MODE: self.on_enter_tag_mode,
            Action.ERASE: self.on_erase,
            Action.COMMIT: self.on_commit,
            Action.AUTO_COMPLETE: self.on_autocomplete,
            Action.UNMAPPED: self.on_type,
        }

    def on_enter_tag_mode(self):
        self.state_container.change_mode(Mode.TAG)
        self.state_container.set_new_tag_input('')

    def on_erase(self):
        current_tag_input = self.state_container.state['new_tag_input']
        self.state_container.set_new_tag_input(current_tag_input[:-1])

    def on_commit(self):
        self.state_container.change_mode(Mode.TAG)
        self.state_container.create_tags_from_input_on_selected_note()
        self.state_container.set_new_tag_input('')
        self.state_container.select_last_tag()
        self.state_container.refresh_notes_list()
        self.state_container.refresh_tag_list()

    def on_autocomplete(self):
        self.state_container.autocomplete_tag_hint()

    def on_type(self, keystroke):
        current_tag_input = self.state_container.state['new_tag_input']
        self.state_container.set_new_tag_input(current_tag_input + keystroke)
