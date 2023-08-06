import sys
from typing import List

import coko.classes.console_parser as console_parser
import coko.classes.sync as sync


def main(args: List=sys.argv[1:])-> None:
    config = console_parser.parse_arguments(args)
    destination_ownerships = sync.register_destination_files(config)
    sync.copy_files(config, destination_ownerships)


if __name__ == "__main__":
    main()

