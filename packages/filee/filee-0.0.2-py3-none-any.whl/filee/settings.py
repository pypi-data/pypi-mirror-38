import os


ENCODING = os.environ.get('FTREE_ENCODING', 'utf-8')

MAX_SIZE = int(os.environ.get('FTREE_MAX_SIZE', 1024 * 1024))
MAX_CHILDREN = int(os.environ.get('FTREE_MAX_CHILDREN', 50))
MAX_DEPTH = int(os.environ.get('FTREE_MAX_DEPTH', 20))

LOAD_FILE_HASHES = os.path.expanduser(
    os.environ.get('FTREE_LOAD_FILE_HASHES', '~/.fileeloadhashes')
)
