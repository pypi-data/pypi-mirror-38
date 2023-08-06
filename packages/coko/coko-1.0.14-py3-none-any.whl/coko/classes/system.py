import sys


def verify_python_version(major_version: int, minor_revision: int)-> None:
    """ Check if current python interpreter version is what we need.
    Compare current interpreter version with the one is provided as needed one.
    If not over needed one version abort execution gracefully warning user
    she is trying to use an unsupported python interpreter.

    :param major_version: Needed major version for Python interpreter.
    :param minor_revision: Needed minor version for Python interpreter.
    :return: None
    """
    if (major_version, minor_revision) > sys.version_info:
        message: str  = f"This program can only be run on Python {major_version}" \
                  f".{minor_version} or newer, you are trying to use Python " \
                  f"{sys.version_info[0]}.{sys.version_info[1]} instead.\nAborting " \
                  "execution."
        sys.exit(message)