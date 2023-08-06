import re


def ellipsis(data, max_length, dots='..'):
    max_length = max_length - len(dots)
    return (data[:max_length] + dots) if len(data) > max_length else data


def strip_markdown(value):
    """Strips markdown. Very basic at this stage, avoiding libraries since
    we only use it for stripping markdown from note titles."""
    return re.sub(r'[#*\-_]\ ?', '', value)
