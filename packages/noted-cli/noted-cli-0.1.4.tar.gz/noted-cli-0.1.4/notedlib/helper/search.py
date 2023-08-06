import re

SEARCHTAG_PATTERN = r'!?\[(.*?)\]'
SEARCHTAG_EXCLUDE_PREFIX_CHAR = '!'


def extract_tags_from_search_term(term: str):
    matches = re.finditer(SEARCHTAG_PATTERN, term)
    include_tags = []
    exclude_tags = []

    for match in matches:
        tag_object = term[match.start():match.end()]
        tag_name = get_tag_name_from_tag_object(tag_object)

        if is_tag_object_of_exclude_type(tag_object):
            exclude_tags.append(tag_name)
        else:
            include_tags.append(tag_name)

    return include_tags, exclude_tags


def is_tag_object_of_exclude_type(tag_object):
    return tag_object.startswith(SEARCHTAG_EXCLUDE_PREFIX_CHAR)


# Note: re.findall does not seem to include the surrounding regex, which is
# intended in this case. Im sure there is a better solution for this though.
def get_tag_name_from_tag_object(tag_object):
    return re.findall(SEARCHTAG_PATTERN, tag_object)[0]


def strip_tags_from_search_term(term: str) -> str:
    return re.sub(SEARCHTAG_PATTERN, '', term).strip()
