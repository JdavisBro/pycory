import json

from contextlib import contextmanager
from pathlib import Path

from .editdict import EditDict

class LevelDataRead(EditDict):
    def __init__(self, content, allowchanges, *args, **kwargs):
        super().__init__(allowchanges, content, *args, **kwargs)

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
                print(level_data["0_0_0"]["geo"])

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
            if True:# getattr(read,"changed",True): # currenly changes are only found if the base dict is modified
                with self.location.open("w") as f:
                    f.writelines(json.dumps(read, separators=(",",":")))
