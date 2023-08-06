from enum import Enum
from operator import attrgetter

from notedlib.database import queryall, queryone, execute
from notedlib.logging import logging

from notedlib.model.note_list_result import NoteListResult
from notedlib.model.note import Note
from notedlib.model.tag import Tag

from notedlib.database import OrderDir
from notedlib.helper.database import get_in_expr_placeholder

logger = logging.getLogger(__name__)


class NoteOrderField(Enum):
    CREATED = 'created_at'
    UPDATED = 'updated_at'
    TITLE = 'title'
    TAGS = 'tags'


def create(note: Note) -> Note:
    logger.debug('Creating note %s' % note)

    execute("""INSERT INTO notes (
            title,
            content,
            created_at,
            updated_at
        ) VALUES(?, ?, DATETIME(?, 'utc'), DATETIME(?, 'utc'))""",
            (note.title, note.content, note.created_at, note.updated_at))
    note.id = queryone('SELECT last_insert_rowid() AS id')['id']
    return note


def read(id: int) -> Note:
    logger.debug('Reading note %s' % id)
    note = Note()
    row = queryone('SELECT * FROM notes WHERE id = ?', (id,))

    if not row:
        return None

    return note.populate(row)


def update(note: Note) -> bool:
    logger.debug('Updating note %s' % note.id)
    execute("""UPDATE notes SET
            title = ?,
            content = ?,
            updated_at = DATETIME('now')
        WHERE id = ?""",
            (note.title, note.content, note.id))
    return True


def delete_by_id(id: int) -> bool:
    logger.debug('Deleting note %s' % id)
    execute('DELETE FROM notes WHERE id = ?', (id,))
    return True


def list_notes(**args):
    query, params = _build_note_list_query(**args)

    logger.debug('List query: %s with params: %s' % (query, params))
    rows = queryall(query, params)
    result = NoteListResult()

    for row in rows:
        result.notes.append(_create_note_from_row(row))

    return result


def _build_note_list_query(**args):
    include_tags = args.get('include_tags', [])
    exclude_tags = args.get('exclude_tags', [])
    term = args.get('term')
    order_by = args.get('order_by', NoteOrderField.CREATED).value
    order_dir = args.get('order_dir', OrderDir.DESC).value

    params = ()
    conditions = []
    joins = []

    if include_tags:
        tag_inclusion_query, tag_inclusion_params = _get_tag_selection_expr(
            include_tags,
            len(include_tags)
        )
        conditions.append(tag_inclusion_query)
        params = params + tag_inclusion_params

    if exclude_tags:
        tag_exclusion_query, tag_exclusion_params = _get_tag_selection_expr(
            exclude_tags,
            0  # None of these tags is allowed to be selected
        )
        conditions.append(tag_exclusion_query)
        params = params + tag_exclusion_params

    if term:
        conditions.append("content LIKE ?")
        params = params + ('%' + term + '%',)

    if include_tags or exclude_tags:
        joins.append('LEFT JOIN notes_tags nt ON nt.note_id = n.id')
        joins.append('LEFT JOIN tags t ON t.id = nt.tag_id')

    condition_str = 'WHERE ' + ' AND '.join(conditions) if conditions else ''
    join_str = '\n'.join(joins)

    query = """
        SELECT
            n.id,
            n.title,
            n.content,
            DATETIME(n.created_at, 'localtime') as created_at,
            DATETIME(n.updated_at, 'localtime') as updated_at,
            (SELECT GROUP_CONCAT(tagname)
             FROM (SELECT t.name as tagname
                   FROM notes_tags nt
                   INNER JOIN tags t ON t.id = nt.tag_id AND nt.note_id = n.id
                   ORDER BY t.name ASC
                  )
            ) AS tags,
            (SELECT GROUP_CONCAT(t.name || '|' || t.id)
             FROM notes_tags nt
             INNER JOIN tags t ON t.id = nt.tag_id AND nt.note_id = n.id
            ) AS serialized_tags
        FROM notes n
        """ + join_str + """
        """ + condition_str + """
        GROUP BY n.id
        ORDER BY %s %s
    """ % (order_by, order_dir)

    return query, params


def _get_tag_selection_expr(tagnames, number_of_matches_required):
    params = tuple(tagnames)
    placeholder_values = (
        get_in_expr_placeholder(len(tagnames)),
        number_of_matches_required
    )

    query = """
        (SELECT COUNT(*)
         FROM notes_tags nt
         INNER JOIN tags t ON t.id = nt.tag_id AND nt.note_id = n.id
         WHERE t.name IN (%s)
        ) = %s""" % placeholder_values

    return query, params


def _create_note_from_row(row) -> Note:
    note = Note(row['content'])
    note.id = row['id']
    note.created_at = row['created_at']
    note.updated_at = row['updated_at']
    note.tags = _unpack_tags(row['serialized_tags'])
    return note


def _unpack_tags(concat_string: str):
    if not concat_string:
        return []

    serialized_tags = concat_string.split(',')
    tags = []

    for serialized_tag in serialized_tags:
        parts = serialized_tag.split('|')
        tag = Tag(parts[0])
        tag.id = int(parts[1])
        tags.append(tag)

    _order_tags_by_name(tags)
    return tags


def _order_tags_by_name(tags) -> None:
    tags.sort(key=attrgetter('name'))
