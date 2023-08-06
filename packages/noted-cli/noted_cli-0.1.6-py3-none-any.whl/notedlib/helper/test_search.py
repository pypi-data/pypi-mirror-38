import unittest

from .search import \
        extract_tags_from_search_term, \
        strip_tags_from_search_term, \
        get_tag_name_from_tag_object


class TestSearchHelper(unittest.TestCase):
    def test_extract_include_tags_from_search_string(self):
        search_term = 'my [cool] search [@home] ![completed]'
        include_tags, exclude_tags = extract_tags_from_search_term(search_term)

        self.assertEqual(include_tags, ['cool', '@home'])
        self.assertEqual(exclude_tags, ['completed'])

    def test_get_tag_name_from_tag_object(self):
        tag_object = '[cool]'
        tag_name = get_tag_name_from_tag_object(tag_object)
        self.assertEqual(tag_name, 'cool')

    def test_strip_tags_from_search_string(self):
        term = '[cool][@home] search string'
        stripped_term = strip_tags_from_search_term(term)
        self.assertEqual(stripped_term, 'search string')


if __name__ == '__main__':
    unittest.main()
