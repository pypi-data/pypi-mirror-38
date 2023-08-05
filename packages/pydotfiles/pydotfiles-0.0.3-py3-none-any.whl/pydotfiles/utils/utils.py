import os.path
import os

"""
Utility classes
"""


class PrettyPrint:
    """
    Wrapper class to have a pretty log output,
    utilizing ANSI escape sequences to do get
    our output
    """

    SUCCESS_GREEN = '\033[92m'
    INFO_BLUE = '\033[94m'
    USER_YELLOW = '\033[0;33m'
    WARN_ORANGE = '\033[38:2:255:165:0m'
    FAIL_RED = '\033[31m'

    # Other settings not turned on yet
    # HEADER = '\033[95m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'

    END_COLOUR = '\033[0m'

    @staticmethod
    def success(message):
        print(f"[ {PrettyPrint.SUCCESS_GREEN}OK{PrettyPrint.END_COLOUR} ] {message}")

    @staticmethod
    def info(message):
        print(f"[{PrettyPrint.INFO_BLUE}INFO{PrettyPrint.END_COLOUR}] {message}")

    @staticmethod
    def user(message):
        print(f"[{PrettyPrint.USER_YELLOW}USER{PrettyPrint.END_COLOUR}] {message}")

    @staticmethod
    def warn(message):
        print(f"[{PrettyPrint.WARN_ORANGE}WARN{PrettyPrint.END_COLOUR}] {message}")

    @staticmethod
    def fail(message):
        print(f"[{PrettyPrint.FAIL_RED}INFO{PrettyPrint.END_COLOUR}] {message}")


"""
Utility functions
"""

def is_linked(origin, destination):
    return os.path.islink(destination) and os.path.realpath(destination) == os.path.realpath(origin)


def symlink_file(origin, destination):
    if is_linked(origin, destination):
        PrettyPrint.success(f"`{origin}` is already symlinked to `{destination}`")
        return

    try:
        os.symlink(origin, destination)
        PrettyPrint.success(f"Successfully symlinked `{origin}` to `{destination}`")
    except Exception as e:
        PrettyPrint.fail(f"Failed to symlink `{origin}` to `{destination}`, error was:\n{e}")
        raise

def unsymlink_file(origin, destination):
    if is_linked(origin, destination):
        try:
            os.unlink(destination)
            PrettyPrint.success(f"Successfully unlinked symlink `{destination}` from `{origin}`")
        except Exception as e:
            PrettyPrint.fail(f"Failed to unlink symlink `{destination}` from `{origin}`, error was:\n{e}")
            raise
    else:
        raise RuntimeError(f"The symlink destination: `{destination}` from `{origin}` does not exist")
