import re  # TODO: This is not part of this abstraction level
from notedlib.model.tag import Tag
from notedlib.model.note import Note
from notedlib.logging import logging
from notedlib.tui.modes.mode_base import Mode, SystemMessage
from notedlib.helper.search import extract_tags_from_search_term, \
    strip_tags_from_search_term

# Enums
from notedlib.database import OrderDir
from notedlib.repository.note import NoteOrderField

logger = logging.getLogger(__name__)


class StateContainer:
    def __init__(self, api, state, editor):
        self.api = api
        self.state = state
        self.editor = editor

    def refresh_notes_list(self):
        result = self.api.list_notes(**self._get_note_list_args())
        self._remember_selected_note_position()
        self.state['notes'] = result.notes
        self._restore_selected_note_position()

    def _get_note_list_args(self):
        search_term = self.state.get('search_term')
        include_tags, exclude_tags = extract_tags_from_search_term(search_term)

        return {
            'term': strip_tags_from_search_term(search_term),
            'order_by': self.state.get('order_by'),
            'order_dir': self.state.get('order_dir'),
            'include_tags': include_tags,
            'exclude_tags': exclude_tags,
        }

    def _remember_selected_note_position(self):
        selected_note = self._get_selected_note()

        if selected_note:
            logger.debug('Remembering selected note: %s' % selected_note.id)
            self.state['selected_note_id'] = selected_note.id

    def _restore_selected_note_position(self):
        remembered_note_id = self.state['selected_note_id']

        if remembered_note_id is not None:
            logger.debug('Restoring selected note: %s' % remembered_note_id)
            note_new_index = self._get_note_index_by_id(remembered_note_id)

            if note_new_index is not None:
                self.state['selected_note_index'] = note_new_index

    def toggle_order_direction(self):
        cur_dir = self.state['order_dir']
        new_dir = OrderDir.DESC if cur_dir == OrderDir.ASC else OrderDir.ASC
        self.state['order_dir'] = new_dir

    def rotate_order_by_field(self):
        order_by_options = [NoteOrderField.CREATED, NoteOrderField.UPDATED,
                            NoteOrderField.TAGS, NoteOrderField.TITLE]
        current_order_by_value = self.state.get('order_by')
        order_by_index = order_by_options.index(current_order_by_value) + 1

        if order_by_index > len(order_by_options) - 1:
            order_by_index = 0

        self.set_order_by_field(order_by_options[order_by_index])

    def set_order_by_field(self, order_by_field: NoteOrderField):
        self.state['order_by'] = order_by_field

    def change_mode(self, mode: Mode):
        self.state['mode'] = mode

    def set_search_term(self, term):
        self.state['search_term'] = term

    def select_prev_note(self):
        self._set_selected_note_index(max(
            0, self.state['selected_note_index'] - 1
        ))

    def select_next_note(self):
        number_of_notes = len(self.state['notes'])
        self._set_selected_note_index(min(
            number_of_notes - 1,
            self.state['selected_note_index'] + 1
        ))

    def select_first_note(self):
        self._set_selected_note_index(0)

    def select_last_note(self):
        self._set_selected_note_index(len(self.state['notes']) - 1)

    def _set_selected_note_index(self, index):
        self.state['selected_note_index'] = index

    def select_prev_tag(self):
        selected_tag_index = self.state['selected_tag_index']
        self.state['selected_tag_index'] = max(0, selected_tag_index - 1)

    def select_next_tag(self):
        selected_note = self._get_selected_note()
        max_tag_index = len(selected_note.tags) - 1

        self.state['selected_tag_index'] = min(
            max_tag_index, self.state['selected_tag_index'] + 1)

    def select_first_tag(self):
        self.state['selected_tag_index'] = 0

    def select_last_tag(self):
        selected_note = self._get_selected_note()
        max_tag_index = len(selected_note.tags) - 1
        self.state['selected_tag_index'] = max_tag_index

    def untag_selected_note_and_tag(self):
        selected_note = self._get_selected_note()
        selected_tag = self._get_selected_tag()

        if not selected_tag:
            return

        self.api.untag_note(note_id=selected_note.id,
                            tag_name=selected_tag.name)

        self.select_prev_tag()

    def create_tags_from_input_on_selected_note(self):
        selected_note = self._get_selected_note()

        # Support for adding multiple tags at once separated with space
        for tag_name in self.state['new_tag_input'].split():
            new_tag = Tag(tag_name)
            self.api.tag_note(note_id=selected_note.id, tag_name=new_tag.name)

    def set_new_tag_input(self, value: str):
        self.state['new_tag_input'] = value
        self.state['new_tag_input_hint'] = self._get_tag_name_hint(value)

    # TODO: Move the nitty-grittys to other, more suiting module
    def _get_tag_name_hint(self, tagname_part: str) -> str:
        selected_note = self._get_selected_note()
        existing_tagnames = [tag.name for tag in selected_note.tags]
        available_tagnames = [tag.name for tag in self.state['tags']]

        # We don't want to show existing tags as hint
        for existing_tagname in existing_tagnames:
            if existing_tagname in available_tagnames:
                available_tagnames.remove(existing_tagname)

        hint = ''

        if len(tagname_part) > 0:
            # We assume that the tags are sorted by name
            r = re.compile('^' + re.escape(tagname_part))
            matches = list(filter(r.match, available_tagnames))
            hint = matches[0] if len(matches) else ''

        return hint

    def edit_content(self):
        selected_note = self._get_selected_note()
        new_content = self.editor.edit_content(selected_note.content)

        if new_content != selected_note.content:
            self.api.update_note(selected_note.id, content=new_content)

    def create_new_note(self):
        new_note_default_content = '# Title'
        content = self.editor.edit_content(new_note_default_content)
        self.api.create_note(content=content)

    def delete_selected_note(self):
        selected_note = self._get_selected_note()
        self.api.delete_note(selected_note.id)

    def _get_note_by_index(self, index) -> Note:
        if index > len(self.state['notes']) - 1:
            return None

        return self.state['notes'][index]

    def _get_note_index_by_id(self, note_id):
        for index, note in enumerate(self.state.get('notes', [])):
            if note.id == note_id:
                return index

        return None

    def _get_selected_note(self) -> Note:
        return self._get_note_by_index(self.state['selected_note_index'])

    def _get_selected_tag(self) -> Tag:
        current_note = self._get_selected_note()
        selected_tag_index = self.state['selected_tag_index']

        if selected_tag_index > len(current_note.tags) - 1:
            return None

        return current_note.tags[self.state['selected_tag_index']]

    def refresh_tag_list(self):
        result = self.api.list_tags(order_by='name')
        self.state['tags'] = result.tags

    def autocomplete_tag_hint(self):
        self.set_new_tag_input(self.state['new_tag_input_hint'])

    # TODO: other way of communicating with rendering, this is dirty
    def append_system_message(self, system_message: SystemMessage):
        system_msq = self.state['system_msq']
        system_msq.append(system_message)
        self.state['system_msq'] = system_msq
