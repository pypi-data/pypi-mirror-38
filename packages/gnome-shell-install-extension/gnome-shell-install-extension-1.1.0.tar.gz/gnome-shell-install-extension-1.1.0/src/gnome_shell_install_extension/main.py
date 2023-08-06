#!/usr/bin/env python3

from json import loads
from pathlib import Path
from sys import argv, stderr
from zipfile import ZipFile


def print_help():
    print("""Usage: gnome-shell-install-extension FILE...
Install the Gnome Shell extension(s) for the current user.

Each FILE must be a valid Gnome Shell extension provided as a zip file.""")


def main():
    ret_code = 0
    
    if len(argv) == 1 or argv[1] in ('-h', '--help'):
        print_help()

    else:
        filenames = argv[1:]
        # Unzip extensions to the user Gnome Shell extension folder
        user_dir = Path.home() / '.local' / 'share' / 'gnome-shell' / 'extensions'
        for filename in filenames:
            with ZipFile(filename) as zip_file:
                # Get the extension UUID from the metadata file inside the zip
                try:
                    with zip_file.open("metadata.json") as metadata:
                        json_data = loads(metadata.read())
                        name = json_data["name"]
                        extension_uuid = json_data["uuid"]
                    zip_file.extractall(path=user_dir / extension_uuid)
                    print("Installed extension: {}".format(name))
                except KeyError as ex:
                    print("Failed to install extension: {}. {}".format(filename, ex), file=stderr)
                    ret_code = 1

    exit(ret_code)
