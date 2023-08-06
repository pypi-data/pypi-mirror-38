import dataclasses
import os
import shutil
from typing import List, Dict

import coko.classes.configuration as configuration


@dataclasses.dataclass
class FileInfo:
    relative_filename_path: str
    ownership: configuration.FileOwnership


def get_files(root_folder: str)-> str:
    """ Iterator to get all files inside a nested folder tree.

    :param root_folder: Base folder where to star getting files from.
    :return: Iterator return files path names relatives to root folder.
    """
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            absolute_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(absolute_path, root_folder)
            yield relative_path


def set_ownership(file_path: str, file_info: configuration.FileOwnership)-> None:
    """ Set file for uid, guid and permissions given through a FileOwnership
    object.

    To use this function application should be run as sudo, otherwise the only
    you'll get is an "Operation not permitted" error.

    :param file_path: Absolute file path whose permissions we want to set.
    :param file_info: UID, GUID and access permission to set for this file.
    :return: None
    """
    os.chown(file_path, file_info.uid, file_info.guid)
    os.chmod(file_path, file_info.permissions)


def register_destination_files(config: configuration.Configuration)-> List[FileInfo]:
    """ Walk through destination folder taking note of relative path and
    permissions of every file it meets.

    :param config: Configuration generated from console parameters.
    :return: A list with a FileInfo object for every file in destination folder.
    """
    destination_files = []
    for destination_file in get_files(config.destination_folder):
        file_info = os.stat(os.path.join(config.destination_folder, destination_file))
        permissions = configuration.FileOwnership(file_info.st_uid,
                                                  file_info.st_gid,
                                                  file_info.st_mode)
        destination_files.append(FileInfo(destination_file,
                                          permissions))
    return destination_files


def _copy(source: str, destination: str, permissions: configuration.FileOwnership)-> None:
    """ Copy a file from source to destination and set at destination given
    permissions.

    :param source: Source absolute file path.
    :param destination: Destination absolute file path.
    :param permissions: File permissions to be set at destination.
    :return: None
    """
    shutil.copy2(source, destination)
    set_ownership(destination, permissions)

    # set_ownership() would not be needed here because shutil.copyfile
    # does not overwrite destination file metadata.
    #
    # shutil.copyfile(absolute_source_path, absolute_destination_path)
    #
    # TODO: Refactor code to remove storing destination files metadata.
    # If shutil.copyfile does not overwrite destination files metadata
    # then register_destination_files does not need to save them
    # before copy process. That leads to the point where I need
    # to think if configuration.FileOwnership, set_ownership() and
    # even register_destination_nodes are actually needed any longer.


def copy_files(config: configuration.Configuration,
               destination_ownerships: List[FileInfo])-> None:
    """ Walks through original folder copying into destination but keeping
    original destination folder files permissions.

    It won't copy a file into destination folder if that folder was not already
    present unless Configuration.ownership was other than None. If
    Configuration.ownership wasn't None then ownership would be a
    configuration.FileOwnership object with permissions every newly created
    file at destination will have by default.

    :param config: configuration generated from console parameters.
    :param destination_ownerships: A list with ownership info for every file at
    destination folder.
    :return: None
    """
    destination_files: Dict[str, configuration.FileOwnership] = {item.relative_filename_path: item.ownership
                                                                 for item in destination_ownerships}
    for source_file in get_files(config.source_folder):
        absolute_source_path = os.path.join(config.source_folder, source_file)
        absolute_destination_path = os.path.join(config.destination_folder, source_file)
        # TODO: Add a timestamp check to copy only updated files.
        if source_file in destination_files:
            # Standard use case: copy only files already present at destination.
            _copy(absolute_source_path, absolute_destination_path,
                  destination_files[source_file])
        elif config.default_ownership is not None:
            # Exceptional case: Create files at destination that were present at
            # source folder but not at destination one. We only get here
            # if "--create" flag was used in console command.
            _copy(absolute_source_path, absolute_destination_path,
                  config.default_ownership)




