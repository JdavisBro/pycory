"""
Path module for finding, editing
"""

import os
import sys
import json

from contextlib import contextmanager
from pathlib import Path

__all__ = (
    "EditDict",
    "Playdata",
    "PlaydataRead",
    "Save",
    "find_save"
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

class Playdata():
    def __init__(self, location: Path):
        self.location = location

    def __str__(self):
        return str(location)

    def make_backups(self, content):
        """
        Makes a backup of _playdata,
        Two backups can exists at once and the oldest will be deleted
        One backup is made when it doesn't exist and is never touched.
        """
        backupDir = (self.location.parent / "pycoryBackups")
        backupDir.mkdir(exist_ok=True)

        if not (backupDir / "_playdata_backup_FIRST").is_file():
            with (backupDir / "_playdata_backup_FIRST").open("w+") as f:
                f.writelines(content)

        (backupDir / "_playdata_backup_2").unlink(missing_ok=True)

        if (backupDir / "_playdata_backup_1").is_file():
            (backupDir / "_playdata_backup_1").rename((backupDir / "_playdata_backup_2"))
        
        with (backupDir / "_playdata_backup_1").open("w+") as f:
            f.writelines(content)

    @contextmanager
    def open(self, mode: str="r"):
        """
        Open _playdata for reading or editing
        Use in a with statement, for example:

            with save.playdata.open("r") as playdata:
                print(playdata.screen)

        mode can be "r" for read-only mode or "w" to enable writing
        writing mode automatically makes a backup
        """
        with self.location.open("r") as f:
            content = f.readlines()
        if mode == "w":
            self.make_backups(content)
        read = PlaydataRead(content, mode=="w")
        yield read
        if mode == "w":
            read.dicts_to_str()
            if read.changed:
                with self.location.open("w") as f:
                    f.writelines(read.content)

class PlaydataRead():
    def __init__(self, content, allowchanges):
        self.content = content
        self.allowchanges = allowchanges
        self.changed = False

    def dicts_to_str(self):
        for i,v in enumerate(self.content):
            if isinstance(v,dict):
                if getattr(v, "changed", False): # getattr for if it's manually overwritten with a normal dict (in which case self.changed would be true anyway)
                    self.changed = True
                self.content[i] = json.dumps(v,separators=(",",":")) + " \n"

    @property
    def screen(self):
        """
        Save's screen location.
        Formatted [layer, x, y]
        """
        return [int(self.content[2][:-2]),int(self.content[0][:-2]),int(self.content[1][:-2])]

    @screen.setter
    def screen(self, value):
        if not self.allowchanges:
            raise IOError("Playdata not opened for writing.")
        if isinstance(value,(list,tuple)):
            if len(value) == 3:
                self.changed = True
                self.content[2], self.content[0], self.content[1] = [str(i) + " \n" for i in value] 
            else:
                raise ValueError("Length of screen value should be 3")
        else:
            raise TypeError("Screen must be set to a list/tuple")

    @property
    def position(self):
        """
        Save's position on screen.
        Formatted [x, y]
        """
        return [float(self.content[4][:-2]),float(self.content[5][:-2])]

    @screen.setter
    def screen(self, value):
        if not self.allowchanges:
            raise IOError("Playdata not opened for writing.")
        if isinstance(value,(list,tuple)):
            if len(value) == 2:
                self.changed = True
                self.content[4], self.content[5] = [str(i) + " \n" for i in value] 
            else:
                raise ValueError("Length of position value should be 2")
        else:
            raise TypeError("Position must be set to a list/tuple")

    def _to_dict(self,line):
        if not isinstance(self.content[line],dict):
            self.content[line] = EditDict(self.allowchanges,json.loads(self.content[line]))
        return self.content[line]

    def _dict_setter(self,line,value):
        if not self.allowchanges:
            raise IOError("Playdata not opened for writing.")
        if isinstance(value,dict):
            self.changed = True
            self.content[line] = value
        else:
            raise TypeError("Value must be set to a dict")

    @property
    def state(self):
        """
        The state line of the save file as a dictionary. (line 4)
        """
        return self._to_dict(3)

    @state.setter
    def state(self,value):
        try:
            self._dict_setter(3, value)
        except TypeError as error:
            raise TypeError("State must be set to a dict")

    @property
    def character_states(self):
        """
        A dictionary of character states. (line 7)
        """
        return self._to_dict(6)

    @character_states.setter
    def character_states(self,value):
        try:
            self._dict_setter(6, value)
        except TypeError as error:
            raise TypeError("Character states must be set to a dict")

    @property
    def decor(self):
        """
        A dictionary of decor. (line 10)
        Formatted { "DECOR NAME": { "x": XPOS, "y": YPOS, "lvl": "SCREEN_X_Y", "flip": 0/1, "time": TIMEINT } }
        """
        return self._to_dict(9)

    @decor.setter
    def decor(self,value):
        try:
            self._dict_setter(9, value)
        except TypeError as error:
            raise TypeError("Decor must be set to a dict")

    @property
    def photos(self):
        """
        A dictionary of photos. (line 14)
        Formatted { "NUMBER based on screen" or "0": ["photo location from paintdog dir"] }
        """
        return self._to_dict(13)

    @photos.setter
    def photos(self,value):
        try:
            self._dict_setter(13, value)
        except TypeError as error:
            raise TypeError("Photos must be set to a dict")

    @property
    def paint(self):
        """
        A dictionary of paint. (line 19)
        Formatted {"layer_x_y.paint": "paintdata"}
        """
        return self._to_dict(18)

    @paint.setter
    def paint(self,value):
        try:
            self._dict_setter(6, value)
        except TypeError as error:
            raise TypeError("Paint must be set to a dict")

class Save():
    def __init__(self, location: Path):
        self.location = location
        self.playdata = Playdata(location / "_playdata")

    def __str__(self):
        return str(self.location)

    def __repr__(self):
        return str(self.location)

def find_save(location=None):
    """
    Returns a save location from first:
      - Location argument
      - `CHICORYSAVEPATH` Environment variable
      - Default save location
    """
    if not location:
        if "CHICORYSAVEPATH" in os.environ:
            isfrom = "Environment"
            location = os.environ["CHICORYSAVEPATH"]

    if not location:
        if sys.platform == "win32" or sys.platform ==  "cygwin":
            save = Path(os.path.expandvars("%LOCALAPPDATA%/paintdog/save/"))
        elif sys.platform == "darwin":
            save = Path("~/Library/Application Support/paintdog/save/").expanduser()
        elif sys.platform == "linux":
            save = Path("~/.local/share/Steam/steamapps/compatdata/1123450/pfx/drive_c/users/steamuser/Local Settings/Application Data/paintdog/save/").expanduser()
        isfrom = "Default"
    else:
        if sys.platform == "win32" or sys.platform == "cygwin":
            save = Path(os.path.expandvars(str(location)))
        else:
            if not isinstance(location,Path):
                save = Path(location)
            save = save.expanduser()
        isfrom = "Argument"
    if save.is_dir():
        return Save(save)
    else:
        return FileNotFoundError(f"Couldn't find save file. (from {isfrom})")