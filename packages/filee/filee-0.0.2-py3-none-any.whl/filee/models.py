import base64
import os
from dataclasses import dataclass
from typing import List, Optional

from . import settings
from .hasher import FileHasher


def raw_to_encoded(b: bytes) -> str:
    return base64.b64encode(b).decode('ascii')


def encoded_to_raw(s: str) -> bytes:
    return base64.b64decode(s)


@dataclass
class FileTree:
    name: str
    content: Optional[str] = None

    too_big: bool = False
    binary: bool = False
    read_only: bool = False
    changed: bool = True

    children: Optional[List[dict]] = None

    TOO_DEEP = 'TOO_DEEP'

    @property
    def is_dir(self):
        return bool(self.children)

    @classmethod
    def load(cls,
             target: Optional[str] = None,
             hasher: Optional[FileHasher] = None,
             _depth: int = 0, _name: str = ''):

        target = target or os.getcwd()
        if _depth > settings.MAX_DEPTH:
            return cls(name=cls.TOO_DEEP)

        read_only = os.access(target, os.R_OK) and not os.access(target, os.W_OK)

        if os.path.isdir(target):
            return cls(
                name=_name,
                children=[cls.load(
                    target=os.path.join(target, n),
                    hasher=hasher,
                    _depth=_depth+1,
                    _name=n,
                ) for n in sorted(os.listdir(target))[:settings.MAX_CHILDREN]],
                read_only=read_only
            )

        with open(target, 'rb') as f:
            content: bytes = f.read(settings.MAX_SIZE + 1)

        if len(content) > settings.MAX_SIZE:
            return cls(
                name=_name,
                too_big=True,
                content=None,
                read_only=read_only,
                binary=True,
            )

        if hasher and not hasher.has_changed(target, content):
            return cls(
                name=_name,
                too_big=False,
                changed=False,
                read_only=read_only,
            )

        try:
            content_str = content.decode(settings.ENCODING)
            binary = False
        except UnicodeDecodeError:
            binary = True
            content_str = raw_to_encoded(content)

        return cls(
            name=_name,
            content=content_str,
            binary=binary,
            too_big=False,
            read_only=read_only
        )

    def save(self, target=None):
        target = target or os.getcwd()
        if not self.is_dir:
            p = os.path.join(target, self.name)

            if self.binary:
                with open(p, mode='wb') as f:
                    f.write(encoded_to_raw(self.content))
            else:
                with open(p, mode='w', encoding='utf-8') as f:
                    f.write(self.content)
        else:
            for c in self.children:
                c.save(os.path.join(target, self.name))

    @classmethod
    def from_dict(cls, d: dict):
        children = d.pop('children', None)

        if not children:
            return cls(
                **d
            )
        return cls(
            children=[cls.from_dict(c) for c in children],
            **d,
        )

    def to_dict(self):
        data = {
            k: getattr(self, k)
            for k in self.__annotations__.keys()
        }
        if not self.is_dir:
            return data
        else:
            children = data.pop('children')
            return {
                'children': [
                    c.to_dict() for c in children
                ],
                **data,
            }
