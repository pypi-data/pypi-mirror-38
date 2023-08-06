import json

import click

from . import settings
from .hasher import FileHasher
from .models import FileTree


@click.command()
@click.option('--dir', default='.', help='Target dir to load')
@click.option('--etag/--no-etag', default=False, help='Use Etag hashing')
def load(dir, etag):
    if etag:
        with FileHasher(settings.LOAD_FILE_HASHES) as hasher:
            ft = FileTree.load(dir, hasher)
    else:
        ft = FileTree.load(dir)
    print(json.dumps(ft.to_dict(), ensure_ascii=False))


@click.command()
def save():
    inp = input()
    data = json.loads(inp)
    ft = FileTree.from_dict(data)
    ft.save()


cli = click.Group()
cli.add_command(save)
cli.add_command(load)
