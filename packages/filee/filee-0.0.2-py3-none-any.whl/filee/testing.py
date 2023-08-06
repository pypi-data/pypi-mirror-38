from . import settings


UNSET = object()


class OverrideSettings:
    def __init__(self, **new_settings):
        self.old_values = {}

        for k, v in new_settings.items():
            self.set(k, v)

    def set(self, attr, value):
        old = getattr(settings, attr, UNSET)
        self.old_values[attr] = old
        setattr(settings, attr, value)

    def revert(self):
        for k, v in self.old_values.items():
            if v is UNSET:
                delattr(settings, k)
            else:
                setattr(settings, k, v)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.revert()
        return self
