"""
Path module for finding, editing
"""

import os
import sys
import json

from contextlib import contextmanager
from pathlib import Path

__all__ = (
    "Playdata",
    "PlaydataRead",
    "Save",
    "find_save"
)

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
        if read.changed:
            read.dicts_to_str()
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
                self.content[i] = json.dumps(v,separators=(",",":")) + " \n"

    @property
    def screen(self):
        """
        Returns save's screen location.
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
        Returns save's position on screen.
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
            self.content[line] = json.loads(self.content[line])
            if self.allowchanges:
                self.changed = True
        return self.content[line]

    @property
    def state(self):
        """
        Returns the state line of the save file as a dictionary. (line 4)
        """
        return self._to_dict(3)

    @property
    def character_states(self):
        """
        Returns a dictionary of character states. (line 7)
        """
        return self._to_dict(6)

    @property
    def decor(self):
        """
        Returns a dictionary of decor. (line 10)
        Formatted { "DECOR NAME": { "x": XPOS, "lvl": "SCREEN_X_Y", "flip": 0/1, "time": TIMEINT, "y": YPOS } }
        """
        return self._to_dict(9)

    @property
    def paint(self):
        """
        Returns a dictionary of paint. (line 19)
        Formatted {"layer_x_y.paint": "paintdata"}
        """
        return self._to_dict(18)

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
      - Specified location
      - `CHICORYSAVEPATH` Environment variable
      - Default save location
    """
    if not location:
        if "CHICORYSAVEPATH" in os.environ:
            location = os.environ["CHICORYSAVEPATH"]

    if not location:
        if sys.platform == "win32" or sys.platform ==  "cygwin":
            save = Path(os.path.expandvars("%LOCALAPPDATA%/paintdog/save/"))
        elif sys.platform == "darwin":
            save = Path("~/Library/Application Support/paintdog/save/").expanduser()
        elif sys.platform == "linux":
            save = Path("~/.local/share/Steam/steamapps/compatdata/1123450/pfx/drive_c/users/steamuser/Local Settings/Application Data/paintdog/save/").expanduser()
    else:
        if sys.platform == "win32" or sys.platform == "cygwin":
            save = Path(os.path.expandvars(str(location)))
        else:
            if not isinstance(location,Path):
                save = Path(location)
            save = save.expanduser()
    if save.is_dir():
        return Save(save)
    else:
        return FileNotFoundError("Couldn't find save file.")