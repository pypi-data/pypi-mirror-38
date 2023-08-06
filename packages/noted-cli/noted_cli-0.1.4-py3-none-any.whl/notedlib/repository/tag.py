from notedlib.database import queryone, queryall, execute
from notedlib.logging import logging
from notedlib.helper.validation import validate_tag_name

from notedlib.model.tag import Tag
from notedlib.model.tag_list_result import TagListResult

logger = logging.getLogger(__name__)


def tag_note(note_id, tag_id):
    """Create relation between note and tag."""
    # Check if the relation already exists
    result = queryone("""SELECT count(*) as c FROM notes_tags
                    WHERE note_id = ? AND tag_id = ?""", (note_id, tag_id))

    if result['c'] > 0:
        return

    logger.debug('Creating relation between note %s and tag %s' %
                 (note_id, tag_id))
    execute('INSERT INTO notes_tags (note_id, tag_id) VALUES(?, ?)',
            (note_id, tag_id))


def untag_note(note_id, tag_id):
    """Remove relation between note and tag."""
    execute('DELETE FROM notes_tags WHERE note_id = ? AND tag_id = ?',
            (note_id, tag_id))
    logger.debug('Removed relation between note %s and tag %s' %
                 (note_id, tag_id))


def ensure_created(names):
    """Ensures that a list of tag names gets created."""
    for name in names:
        validate_tag_name(name)

    placeholder = ','.join('?' * len(names))
    query = ('SELECT * FROM tags WHERE name IN(%s)' % placeholder)
    rows = queryall(query, tuple(names))
    tags = []

    for name in names:
        tag_row = next((row for row in rows if row['name'] == name), None)

        if tag_row:
            tag = Tag()
            tag.populate(tag_row)
        else:
            tag = Tag(name)
            tag = create(tag)

        tags.append(tag)

    return tags


def create(tag):
    query = ('INSERT INTO tags (name) VALUES(?)')
    execute(query, (tag.name,))
    tag.id = queryone('SELECT last_insert_rowid() AS id')['id']
    logger.debug('Created tag %s' % tag)
    return tag


def read(id, user_id):
    logger.debug('Reading tag %s' % id)
    query = 'SELECT * FROM tags WHERE id = ?'
    row = queryone(query, (id,))

    if not row:
        return None

    tag = Tag()
    tag.populate(row)
    return tag


def update(tag):
    logger.debug('Update tag %s with new name %s' % (tag.id, tag.name))
    execute('UPDATE tags SET name = ? WHERE id = ?', (tag.name, tag.id))
    return True


def delete(tag_id):
    logger.debug('Deleting tag %s' % tag_id)
    execute('DELETE FROM tags WHERE id = ?', (tag_id,))


def list_tags(**kwargs):
    order_by = kwargs.get('order_by', 'id')
    order_dir = kwargs.get('order_dir', 'asc')
    query = 'SELECT * FROM tags ORDER BY %s %s' % (order_by,
                                                   order_dir)
    rows = queryall(query)
    result = TagListResult()

    for row in rows:
        tag = Tag()
        tag.populate(row)
        result.tags.append(tag)

    return result


def get_all_for_note(note_id):
    query = ('SELECT t.* from notes as n INNER JOIN notes_tags nt '
             'ON n.id = nt.note_id INNER JOIN tags t '
             'ON nt.tag_id = t.id WHERE n.id = ?')
    rows = queryall(query, (note_id,))
    tags = []

    for row in rows:
        tag = Tag()
        tag.populate(row)
        tags.append(tag)

    return tags
