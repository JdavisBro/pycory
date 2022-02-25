"""
Path module for finding, editing
"""

import os
import sys
import json

from contextlib import contextmanager
from pathlib import Path

from .playdata import *
from .level_data import *

__all__ = (
    "PlaydataRead",
    "Playdata",
    "Save",
    "find_save",
    "ScreenExits",
    "LevelDataScreen",
    "LevelDataRead",
    "LevelData",
    "find_level_data",
)

class Save():
    def __init__(self, location: Path):
        self.location = location
        self.playdata = Playdata(location / "_playdata")

    def __str__(self):
        return str(self.location)

    def __repr__(self):
        return str(self.location)

def find_save(location=None) -> Save:
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
        raise FileNotFoundError(f"Couldn't find save file. (from {isfrom})")

def find_level_data(location=None) -> LevelData:
    """
    Returns a save location from first:
      - Location argument
      - `CHICORYLEVELDATAPATH` Environment variable
      - Default level_data location
    """
    if not location:
        if "CHICORYLEVELDATAPATH" in os.environ:
            isfrom = "Environment"
            location = os.environ["CHICORYLEVELDATAPATH"]

    if not location:
        if sys.platform == "win32" or sys.platform ==  "cygwin":
            level_data = Path("/Program Files (x86)/Steam/steamapps/common/Chicory A Colorful Tale/PC/level_data")
        elif sys.platform == "darwin":
            level_data = Path("~/Library/Application Support/Steam/steamapps/common/Chicory A Colorful Tale/PC/level_data").expanduser()
        elif sys.platform == "linux":
            level_data = Path("~/.local/share/Steam/steamapps/common/Chicory A Colorful Tale/PC/level_data").expanduser()
        isfrom = "Default"
    else:
        if sys.platform == "win32" or sys.platform == "cygwin":
            level_data = Path(os.path.expandvars(str(location)))
        else:
            if not isinstance(location,Path):
                level_data = Path(location)
            level_data = level_data.expanduser()
        isfrom = "Argument"
    if level_data.is_file():
        return LevelData(level_data)
    else:
        raise FileNotFoundError(f"Couldn't find level_data file. (from {isfrom})")
