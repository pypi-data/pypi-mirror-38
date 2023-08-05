import dataclasses
import os.path
from typing import List

import coko.classes.exceptions as exceptions


@dataclasses.dataclass
class FileOwnership:
    uid: int
    guid: int
    permissions: int
    permissions_octal: bool = dataclasses.field(default=False)

    def __post_init__(self)-> None:
        # We let user to enter permissions in octal but we convert to int
        # because system functions we use deal with them as int.
        #
        # User only would enter permissions in octal in automated tests
        # contexts. In production coko will get native permissions
        # directly from files, so what it would read would be int (from st_mode).
        if self.permissions_octal:
            self.permissions = int(str(self.permissions), 8)

    def __eq__(self, other)-> bool:
        # permissions_octal should not be compared for equality because it is
        # not actually related to file but just a switch to create automated
        # tests. If we would let default __eq__ automated test would fail.
        return all([self.uid == other.uid,
                    self.guid == other.guid,
                    self.permissions == other.permissions])


class Folder(object):
    """A descriptor that sets and returns system folders checking folder
    actually exists.
    """
    def __init__(self):
        self._folder_path: str = None

    def __get__(self, obj, objtype)-> str:
        return self._folder_path

    def __set__(self, obj, value):
        absolute_path: str = os.path.abspath(value)
        if os.path.isdir(absolute_path):
            self._folder_path: str = os.path.abspath(value)
        else:
            raise exceptions.FolderNotFound(absolute_path)


class Configuration:
    source_folder: Folder = Folder()
    destination_folder: Folder = Folder()

    def __init__(self, source_folder: str, destination_folder: str,
                 default_ownership: List):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        if default_ownership is not None:
            self.default_ownership: FileOwnership = FileOwnership(default_ownership[0],
                                                                  default_ownership[1],
                                                                  default_ownership[2],
                                                                  default_ownership[3])
        else:
            self.default_ownership = None


