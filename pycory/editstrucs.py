__all__ = (
    "EditDict",
    "EditList",
)

class EditDict(dict):
    def __init__(self, allowchanges, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowchanges = allowchanges
        self._changed = False

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if self.allowchanges:
            if isinstance(value, dict):
                value = EditDict(self.allowchanges,value)
            elif isinstance(value, list):
                value = EditList(self.allowchanges,value)
            super().__setitem__(key, value)
        return value

    def __setitem__(self, key, val):
        if not self.allowchanges:
            raise IOError("Dict not opened for writing.")
        super().__setitem__(key, val)
        self._changed = True

    def update(self, *args, **kwargs):
        if not self.allowchanges:
            raise IOError("Dict not opened for writing.")
        super().update(*args, **kwargs)
        self._changed = True

    @property
    def changed(self) -> bool:
        if self._changed:
            return True
        for i in self:
            if isinstance(i,(EditList,EditDict)):
                if i.changed:
                    return True
        return False

class EditList(list):
    def __init__(self, allowchanges, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowchanges = allowchanges
        self._changed = False

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if self.allowchanges:
            if isinstance(value, dict):
                value = EditDict(self.allowchanges,value)
            elif isinstance(value, list):
                value = EditList(self.allowchanges,value)
            super().__setitem__(key, value)
        return value

    def __setitem__(self, i, value):
        if not self.allowchanges:
            raise IOError("List not opened for writing")
        super().__setitem__(i, value)
        self._changed = True

    def __add__(self, x):
        if not self.allowchanges:
            raise IOError("List not opened for writing")
        super().__add__(x)
        self._changed = True

    def __delitem__(self, i):
        if not self.allowchanges:
            raise IOError("List not opened for writing")
        super().__delitem__(i)
        self._changed = True

    @property
    def changed(self):
        for i in self:
            if isinstance(i,(EditList,EditDict)):
                if i.changed:
                    return True
        return self._changed
