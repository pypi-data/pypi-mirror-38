"""Validation"""
import re
from notedlib.exception import InvalidTagNameException


def validate_tag_name(value):
    if not re.match(r"^[a-zA-Z0-9_\-\@#]*$", value):
        raise InvalidTagNameException("Invalid tag name '%s'" % value)
