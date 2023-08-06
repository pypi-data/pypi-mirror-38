import hashlib
import json
import os


class FileHasher:
    def __init__(self, path, hashes=None):
        self.path = path
        self.hashes = hashes or {}
        self.changed = False

    def load_hash(self):
        if not os.path.exists(self.path):
            return

        with open(self.path) as f:
            c = f.read()

        try:
            self.hashes = json.loads(c)
        except json.JSONDecodeError:
            return

    def save_hash(self):
        if not self.changed:
            return

        with open(self.path, 'w') as f:
            try:
                f.write(json.dumps(self.hashes, ensure_ascii=False))
            except TypeError:
                return

    def __enter__(self):
        self.load_hash()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_hash()

    def calc_hash(self, content: bytes):
        m = hashlib.md5()
        m.update(content)
        return m.hexdigest()

    def has_changed(self, path: str, content: bytes):
        path = os.path.abspath(path)

        h = self.calc_hash(content)

        if path not in self.hashes or self.hashes[path] != h:
            self.changed = True
            self.hashes[path] = h
            return True

        return False
