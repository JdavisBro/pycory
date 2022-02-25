import json
import shutil

from typing import Union
from contextlib import contextmanager
from pathlib import Path

from .editstrucs import EditDict, EditList

__all__ = (
    "ScreenExits",
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
    def __init__(self, content, allowchanges):
        self._changed = False
        self.content = content
        self.allowchanges = allowchanges
        self.exits = ScreenExits(content.get("exits","1111"),False)
        self.objects = EditList(allowchanges,content.get("objects",[]))
        self.decos = EditList(allowchanges,content.get("decos",[]))

    def to_dict(self) -> dict:
        if self.exits.changed:
            self.content["exits"] = str(self.exits)

        if self.objects.changed:
            self.content["objects"] = self.objects

        if self.decos.changed:
            self.content["decos"] = self.decos

        return self.content 

    @property
    def changed(self) -> bool:
        return bool(self._changed or self.exits.changed or self.objects.changed or self.decos.changed)

    def _set(self, key, value):
        if not self.allowchanges:
            raise IOError("level_data is not open for writing")
        self.content[key] = value
        self._changed = True

    @property
    def ambiance(self) -> str:
        """
        The ambiance value of the screen
        Example: "amb_luncheon_outdoor"
        """
        return self.content.get("ambiance",None)

    @ambiance.setter
    def ambiance(self, value: str):
        self._set("ambiance",str(value))

    @property
    def geo(self) -> str:
        """
        The geo *string* of the screen
        """
        return self.content.get("geo", None)

    @geo.setter
    def geo(self, value: str):
        self._set("geo",str(value))

    @property
    def palette(self) -> str:
        return self.content.get("palette",None)

    @palette.setter
    def palette(self, value: str):
        self._set("palette",str(value))

    @property
    def title(self) -> str:
        return self.content.get("title",None)

    @title.setter
    def title(self, value: str):
        self._set("title",str(value))

    @property
    def area(self) -> str:
        return self.content.get("area",None)

    @area.setter
    def area(self, value: str):
        self._set("area",str(value))

    @property
    def transition(self) -> int:
        return int(self.content.get("transition",0))

    @transition.setter
    def transition(self, value: int):
        self._set("transition",int(value))

    @property
    def music(self):
        return self.content.get("music",None)

    @music.setter
    def music(self, value: str):
        self._set("music",str(value))

    @property
    def object_id(self) -> int:
        return int(self.content.get("object_id",None))

    @object_id.setter
    def object_id(self, value: int):
        self._set("object_id",int(value))

    @property
    def name(self) -> str:
        return self.content.get("name",None)

    @name.setter
    def name(self, value: str):
        self._set("name",str(value))

class LevelDataRead(EditDict):
    def __init__(self, content, allowchanges, *args, **kwargs):
        super().__init__(allowchanges, content, *args, **kwargs)

    def to_dict(self):
        for screen in self:
            item = super().__getitem__(screen)
            if isinstance(item, LevelDataScreen):
                if item.changed:
                    self._changed = True
                super().__setitem__(screen, item.to_dict())

    def to_leveldatascreen(self, key, value):
        if not isinstance(value, LevelDataScreen):
            value = LevelDataScreen(value,self.allowchanges)
            super().__setitem__(key, value)
        return value

    def __getitem__(self, key):
        value = self.to_leveldatascreen(key, super().__getitem__(key))
        return value

    def __setitem__(self, key, value: dict): # If you set a screen like level_data[screen] = {}
        if isinstance(value,dict):
            self.to_leveldatascreen(key, value)
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
        One backup is made when it doesn't exist and is never touched.
        """
        if not (self.location.parent / "level_data_backup").is_file():
            print("Pycory | Making level_data backup.")
            shutil.copy(self.location,(self.location.parent / "level_data_backup")) 

    @contextmanager
    def open(self, mode: str="r", backup=True) -> LevelDataRead:
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
            if getattr(read, "to_dict"):
                read.to_dict()
            if getattr(read,"changed",True): # currenly changes are only found if the base dict is modified
                with self.location.open("w") as f:
                    f.write(json.dumps(read,separators=(",",":")))
