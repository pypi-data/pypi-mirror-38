from notedlib.model.base import Base


class Tag(Base):
    def __init__(self, name: str = None):
        self.name = name
        self.id = None

    def to_raw(self):
        return {
            'name': self.name,
            'id': self.id,
        }
