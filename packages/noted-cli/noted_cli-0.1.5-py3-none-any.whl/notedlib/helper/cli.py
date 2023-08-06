import argparse

from notedlib.helper.date import parse_timestamp_string


def parse_tag_string(value: str):
    """Parses comma-separated string of tags into array of tags"""
    if not value:
        return []

    return [part.strip() for part in value.split(',')]


def validate_timestamp_string(value: str):
    try:
        return parse_timestamp_string(value)
    except ValueError:
        msg = "Not a valid date: '%s'" % value
        raise argparse.ArgumentTypeError(msg)
