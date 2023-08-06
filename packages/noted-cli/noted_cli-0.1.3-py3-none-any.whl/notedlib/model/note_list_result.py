from notedlib.model.base import Base


class NoteListResult(Base):
    def __init__(self):
        self.notes = []

    def to_raw(self):
        return {
            'notes': [note.to_raw() for note in self.notes],
        }
