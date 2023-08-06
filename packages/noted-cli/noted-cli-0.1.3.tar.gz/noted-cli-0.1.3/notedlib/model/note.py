from notedlib.model.base import Base
from notedlib.exception import ForbiddenSetterException
from notedlib.helper.string import strip_markdown
from notedlib.helper.date import parse_timestamp_string
from datetime import datetime


class Note(Base):
    def __init__(self, content: str = None):
        self._title = None
        self._content = None
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self.tags = []
        self.id = None

        # Use the setter to set the title as well
        if content:
            self.content = content

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        raise ForbiddenSetterException('Title is determined by content')

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content: str):
        self._content = content
        lines = self._content.splitlines()
        self._title = strip_markdown(
            lines[0]) if len(lines) else 'Unnamed note'

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, string_value):
        self._created_at = parse_timestamp_string(string_value)

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, string_value):
        self._updated_at = parse_timestamp_string(string_value)

    def populate(self, data):
        self.content = data.get('content')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.tags = data.get('tags', [])
        self.id = data.get('id')
        return self

    def to_raw(self):
        return {
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': [tag.to_raw() for tag in self.tags],
            'id': self.id,
        }

    def get_content_preview(self):
        """Returns the content without the title-part"""
        lines = self.content.splitlines()
        return ' '.join(lines[1:])
