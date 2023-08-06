from notedlib.model.base import Base


class NoteTag(Base):
    def __init__(self, note_id, tag_id):
        self.note_id = note_id
        self.tag_id = tag_id
        self.id = None
