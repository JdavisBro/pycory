import json

from typing import Union
from contextlib import contextmanager
from pathlib import Path

from .editdict import EditDict

__all__ = (
    "LevelDataScreen",
    "LevelDataRead",
    "LevelData",
)

class ScreenExits():
    """
    Sets which screens are preloaded when the player is on the this screen.
    (up, down, left, and right)

    Down can be a string from level_data ("1111"/"0000") or a bool to use values from your arguments
    By default (no value provided) all are True (down included)

    If down is a string then up is used to decide whether the provided value should be used to figure out whether it has been changed, leave this as true or the value won't be saved
    """
    def __init__(self, down: Union[str,bool]=True, up: bool=True, left: bool=True, right: bool=True):
        if isinstance(down,str): # idk about this maybe it sucks i think
            if up:
                self.old = ""
            else:
                self.old = down
            self.down = down[0]
            self.up = down[1]
            self.left = down[2]
            self.right = down[3]
        else:
            self.old = "" # If value is provided it should be .changed 
            self.down = down
            self.up = up
            self.left = left
            self.right = right

    def __str__(self):
        return "".join([str(int(i)) for i in [self.down,self.up,self.left,self.right]])

    @property
    def changed(self):
        return self.old != str(self)

class LevelDataScreen():
    def __init__(self, content):
        self.changed = False
        self.content = content
        self.exits = ScreenExits(content.get("exits","1111"),False)

    def to_dict(self):
        if self.exits.changed:
            self.content["exits"] = str(self.exits)

        return self.content 

    def check_changes(self):
        if self.changed:
            return True
        if self.exits.changed:
            return True
        return False

    @property
    def ambiance(self):
        """
        The ambiance value of the screen
        Example: "amb_luncheon_outdoor"
        """
        return self.content.get("ambiance",None)

    @ambiance.setter
    def ambiance(self, value: str):
        self.content["ambiance"] = str(value)
        self.changed = True

    @property
    def geo(self):
        """
        The geo *string* of the screen
        """
        return self.content.get("geo", None)

    @geo.setter
    def geo(self, value: str):
        self.content["geo"] = str(value)
        self.changed = True

class LevelDataRead(EditDict):
    def __init__(self, content, allowchanges, *args, **kwargs):
        super().__init__(allowchanges, content, *args, **kwargs)

    def __str__(self):
        for screen in self:
            item = super().__getitem__(screen)
            if isinstance(item, LevelDataScreen):
                if item.changed:
                    self.changed = True
                super().__setitem__(screen, item.to_dict())
        return json.dumps(self,separators=(",",":"))

    def to_leveldatascreen(self, key, value):
        if not isinstance(value, LevelDataScreen):
            value = LevelDataScreen(value)
            super().__setitem__(key, value)
        return value

    def __getitem__(self, key):
        value = self.to_leveldatascreen(key, super().__getitem__(key))
        return value

    def __setitem__(self, key, value: dict): # If you set a screen like level_data[screen] = {}
        if isinstance(value,dict):
            value = self.to_leveldatascreen(key, value)
        else:
            TypeError("LevelDataScreens must be set to a dict")

class LevelData():
    def __init__(self, location: Path):
        self.location = location

    def __str__(self):
        return str(location)

    def make_backups(self, content):
        """
        Makes a backup of level_data,
        Two backups can exists at once and the oldest will be deleted
        One backup is made when it doesn't exist and is never touched.
        """
        if not (self.location.parent / "level_data_backup").is_file():
            with (self.location.parent / "level_data_backup").open("w+") as f:
                print("Pycory | Making level_data backup.")
                f.writelines(content)

    @contextmanager
    def open(self, mode: str="r", backup=True):
        """
        Open level_data for reading or editing
        Use in a with statement, for example:

            with pycory.get_level_data().open("r") as level_data:
                print(level_data["0_0_0"].geo)

        mode can be "r" for read-only mode or "w" to enable writing
        writing mode automatically makes a backup
        """
        with self.location.open("r") as f:
            content = f.read()
        if mode == "w" and backup:
            self.make_backups(content)
        read = LevelDataRead(json.loads(content), mode=="w")
        yield read
        if mode == "w":
            if getattr(read,"changed",True): # currenly changes are only found if the base dict is modified
                with self.location.open("w") as f:
                    f.write(str(read))
