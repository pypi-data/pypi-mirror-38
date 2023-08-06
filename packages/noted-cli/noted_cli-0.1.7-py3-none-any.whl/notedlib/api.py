from .model.note import Note
from .model.tag import Tag

import notedlib.repository.note as note_repo
import notedlib.repository.tag as tag_repo

from .exception import EnsureTagCreationException


class API:
    def create_note(self, **kwargs):
        note = Note(kwargs.get('content'))
        self._apply_optional_note_arguments(note, kwargs)
        note_repo.create(note)

        tagnames = kwargs.get('tags', [])

        if tagnames:
            tags = tag_repo.ensure_created(tagnames)

            for tag in tags:
                tag_repo.tag_note(note.id, tag.id)

    def _apply_optional_note_arguments(self, note, args):
        if args.get('created_at'):
            note._created_at = args.get('created_at')

        if args.get('updated_at'):
            note._updated_at = args.get('updated_at')

    def read_note(self, id):
        note = note_repo.read(id)

        if not note:
            return None

        note.tags = tag_repo.get_all_for_note(id)
        return note

    def update_note(self, id, **kwargs):
        note = Note(kwargs.get('content'))
        note.id = id
        return note_repo.update(note)

    def delete_note(self, id):
        return note_repo.delete_by_id(id)

    def list_notes(self, **kwargs):
        return note_repo.list_notes(**kwargs)

    def create_tag(self, **kwargs):
        tags = tag_repo.ensure_created([kwargs.get('name')])
        return tags[0] if len(tags) else None

    def read_tag(self, id):
        tag = tag_repo.read(id)
        return tag if tag else None

    def update_tag(self, id, **kwargs):
        tag = Tag(kwargs.get('name'))
        tag.id = id
        return tag_repo.update(tag)

    def tag_note(self, **kwargs):
        note_id = kwargs.get('note_id')
        tags = tag_repo.ensure_created([kwargs.get('tag_name')])

        if not len(tags):
            raise EnsureTagCreationException('Could not ensure tag creation')

        return tag_repo.tag_note(note_id, tags[0].id)

    # TODO: Do not create tags, read only instead
    def untag_note(self, **kwargs):
        note_id = kwargs.get('note_id')
        tags = tag_repo.ensure_created([kwargs.get('tag_name')])

        if not len(tags):
            raise EnsureTagCreationException('Could not ensure tag creation')

        return tag_repo.untag_note(note_id, tags[0].id)

    def delete_tag(self, id):
        return tag_repo.delete(id)

    def list_tags(self, **kwargs):
        return tag_repo.list_tags(**kwargs)
