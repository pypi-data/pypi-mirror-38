import unittest
from unittest.mock import Mock, MagicMock

from .state_container import StateContainer
from .tui import get_initial_state

from notedlib.model.note import Note
from notedlib.model.tag import Tag
from notedlib.model.tag_list_result import TagListResult
from notedlib.model.note_list_result import NoteListResult
from notedlib.database import OrderDir
from notedlib.repository.note import NoteOrderField


class TestStateContainer(unittest.TestCase):
    def setUp(self):
        self.api_mock = Mock()
        self.editor_mock = Mock()
        initial_state = get_initial_state()
        initial_state['notes'] = self._create_mock_notes()
        initial_state['tags'] = self._get_all_tags_from_notes(
            initial_state['notes'])
        self.sc = StateContainer(
            self.api_mock, initial_state, self.editor_mock)

    def _create_mock_notes(self, amount=3):
        notes = []
        for x in range(amount):
            note = Note('some content for note %s' % x)
            note.id = x
            note.tags = self._create_mock_tags('note-%s' % x)
            notes.append(note)

        return notes

    def _create_mock_tags(self, base_name, amount=3):
        tags = []

        for x in range(amount):
            tag = Tag('%s-%s' % (base_name, x))
            tag.id = x
            tags.append(tag)

        return tags

    def _get_all_tags_from_notes(self, notes):
        tags = []
        [tags.extend(note.tags) for note in notes]
        return tags

    def test_toggle_order_direction_should_toggle_order_direction(self):
        assert self.sc.state['order_dir'] == OrderDir.DESC
        self.sc.toggle_order_direction()
        assert self.sc.state['order_dir'] == OrderDir.ASC
        self.sc.toggle_order_direction()
        assert self.sc.state['order_dir'] == OrderDir.DESC

    def test_rotate_order_by_field_should_continue_on_first(self):
        number_of_order_by_fields = len(NoteOrderField)
        initial_sort_option_field = self.sc.state['order_by']

        for x in range(number_of_order_by_fields):
            self.sc.rotate_order_by_field()

        assert self.sc.state['order_by'] == initial_sort_option_field

    def test_refresh_notes_list_should_keep_same_note_selected(self):
        note_list_result = NoteListResult()
        note_list_result.notes = list(reversed(self.sc.state['notes']))
        self.api_mock.list_notes = MagicMock(return_value=note_list_result)

        selected_note_id_before = self.sc.state['notes'][
                self.sc.state['selected_note_index']].id

        self.sc.refresh_notes_list()

        selected_note_id_after = self.sc.state['notes'][
                self.sc.state['selected_note_index']].id

        self.assertEqual(selected_note_id_before, selected_note_id_after)

    def test_refresh_notes_list_should_not_restore_removed_note_position(self):
        note_list_result = NoteListResult()
        note_list_result.notes = self.sc.state['notes'].copy()
        del note_list_result.notes[0]
        self.api_mock.list_notes = MagicMock(return_value=note_list_result)

        selected_note_id_before = self.sc.state['notes'][
                self.sc.state['selected_note_index']].id

        self.sc.refresh_notes_list()

        selected_note_id_after = self.sc.state['notes'][
                self.sc.state['selected_note_index']].id

        self.assertEqual(selected_note_id_before, 0)
        self.assertEqual(selected_note_id_after, 1)

    def test_select_previous_note_should_not_go_beyond_first(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.select_prev_note()
        assert self.sc.state['selected_note_index'] == 0

    def test_select_next_note_should_not_go_beyond_last(self):
        last_note_index = len(self.sc.state['notes']) - 1
        self.sc.state['selected_note_index'] = last_note_index
        self.sc.select_next_note()
        self.assertEqual(self.sc.state['selected_note_index'], last_note_index)

    def test_select_previous_tag_should_not_go_beyond_first(self):
        self.sc.state['selected_tag_index'] = 0
        self.sc.select_prev_tag()
        self.assertEqual(self.sc.state['selected_tag_index'], 0)

    def test_select_next_tag_should_not_go_beyond_last(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.state['selected_tag_index'] = 2
        self.sc.select_next_tag()
        self.assertEqual(self.sc.state['selected_tag_index'], 2)

    def test_select_last_tag_should_select_last_tag(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.select_last_tag()
        self.assertEqual(self.sc.state['selected_tag_index'], 2)

    def test_select_first_tag_should_select_first_tag(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.state['selected_tag_index'] = 2
        self.sc.select_first_tag()
        self.assertEqual(self.sc.state['selected_tag_index'], 0)

    def test_untag_select_note_and_tag_should_call_api(self):
        self.sc.state['selected_note_index'] = 1
        self.sc.state['selected_tag_index'] = 1
        self.sc.untag_selected_note_and_tag()
        self.api_mock.untag_note.assert_called_with(
            note_id=1, tag_name='note-1-1')

    def test_untag_selected_note_and_tag_should_select_previous_tag(self):
        self.sc.state['selected_note_index'] = 1
        self.sc.state['selected_tag_index'] = 2
        self.sc.untag_selected_note_and_tag()
        self.assertEqual(self.sc.state['selected_tag_index'], 1)

    def test_create_tags_from_input_on_selected_note_should_call_api(self):
        self.sc.state['new_tag_input'] = 'two tags'
        self.sc.create_tags_from_input_on_selected_note()

        self.api_mock.tag_note.assert_any_call(
            note_id=0, tag_name='two')
        self.api_mock.tag_note.assert_any_call(
            note_id=0, tag_name='tags')

    def test_set_new_tag_input_should_set_tag_name_hint(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.set_new_tag_input('note-1')
        self.assertEqual(self.sc.state['new_tag_input_hint'], 'note-1-0')

    def test_set_new_tag_input_should_not_hint_about_existing_tagnames(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.set_new_tag_input('note-0')
        self.assertEqual(self.sc.state['new_tag_input_hint'], '')

    def test_edit_content_should_open_editor_with_note_content(self):
        self.sc.edit_content()
        self.editor_mock.edit_content.assert_called_with('some content for note 0')

    def test_edit_content_should_call_api_if_content_was_changed(self):
        self.editor_mock.edit_content = MagicMock(return_value='new content!')
        self.sc.edit_content()
        self.api_mock.update_note.assert_called_with(0, content='new content!')

    def test_create_new_note_should_open_editor(self):
        self.editor_mock.edit_content = MagicMock(return_value='new note!')
        self.sc.create_new_note()
        self.editor_mock.edit_content.assert_called_with('# Title')

    def test_create_new_note_should_call_api(self):
        self.editor_mock.edit_content = MagicMock(return_value='new note!')
        self.sc.create_new_note()
        self.api_mock.create_note.assert_called_with(content='new note!')

    def test_delete_selected_note_should_call_api(self):
        self.sc.state['selected_note_index'] = 0
        self.sc.delete_selected_note()
        self.api_mock.delete_note.assert_called_with(0)

    def test_refresh_tag_list_should_populate_state_from_api(self):
        tag = Tag('@home')
        tag.id = 3
        tag_list_result = TagListResult()
        tag_list_result.tags = [tag]
        self.api_mock.list_tags = MagicMock(return_value=tag_list_result)
        self.sc.refresh_tag_list()
        self.api_mock.list_tags.assert_called_with(order_by='name')
        self.assertEqual(self.sc.state['tags'][0], tag)

    def test_autocomplete_tag_hint_should_apply_hint(self):
        self.sc.set_new_tag_input('note-1')
        self.sc.autocomplete_tag_hint()
        self.assertEqual(
                self.sc.state['new_tag_input'],
                self.sc.state['new_tag_input_hint'])

if __name__ == '__main__':
    unittest.main()
