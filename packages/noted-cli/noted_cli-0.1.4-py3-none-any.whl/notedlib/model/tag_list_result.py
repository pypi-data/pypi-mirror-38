from notedlib.model.base import Base


class TagListResult(Base):
    def __init__(self):
        self.tags = []

    def to_raw(self):
        return {
            'tags': [tag.to_raw() for tag in self.tags],
        }
