import tempfile
import os
from subprocess import call

EDITOR = os.environ.get('EDITOR', 'vi')


# TODO: Curses doesn't seem to clean up after itself when
# launching vim.
def edit_content(content, ext='md'):
    """Opens up the default editor to edit content."""
    data = bytearray(content, 'utf-8')
    with tempfile.NamedTemporaryFile(suffix='.tmp.' + ext) as tf:
        tf.write(data)
        tf.flush()
        call([EDITOR, tf.name])

        tf.seek(0)
        return tf.read().decode('utf-8')
