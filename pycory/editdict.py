__all__ = (
    "EditDict",
)

class EditDict(dict):
    def __init__(self, allowchanges, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowchanges = allowchanges
        self.changed = False

    def __setitem__(self, key, val):
        if not self.allowchanges:
            raise IOError("Dict not opened for writing.")
        super().__setitem__(key, val)
        self.changed = True

    def update(self, *args, **kwargs):
        if not self.allowchanges:
            raise IOError("Dict not opened for writing.")
        super().update(*args, **kwargs)
        self.changed = True
