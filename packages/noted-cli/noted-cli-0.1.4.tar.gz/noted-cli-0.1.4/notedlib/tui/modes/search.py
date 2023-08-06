from .mode_base import ModeBase, Mode, Action


class SearchModeHandler(ModeBase):
    def get_action_map(self):
        return {
            Action.ENTER_NORMAL_MODE: self.on_enter_normal_mode,
            Action.ERASE: self.on_erase,
            Action.COMMIT: self.on_commit,
            Action.UNMAPPED: self.on_type,
        }

    def on_enter_normal_mode(self):
        self.state_container.change_mode(Mode.NORMAL)
        self.state_container.set_search_term('')
        self.state_container.refresh_notes_list()

    def on_erase(self):
        current_term = self.state_container.state['search_term']
        self.state_container.set_search_term(current_term[:-1])

    def on_commit(self):
        self.state_container.change_mode(Mode.NORMAL)
        self.state_container.select_first_note()
        self.state_container.refresh_notes_list()

    def on_type(self, keystroke):
        current_term = self.state_container.state['search_term']
        self.state_container.set_search_term(current_term + keystroke)
