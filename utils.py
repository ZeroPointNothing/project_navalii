import os
import sys
import time


def cls():
    """
    Clears the screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class Logger:
    """
    Logger.
    """

    def __init__(self):
        self.name = "NAVA"

    def info(self, text: str | None) -> None:
        """
        For general information.
        """
        if not text:
            return

        print(f"[{time.strftime('%H:%M:%S')}] {self.name}: " + text)
        sys.stdout.flush()

    def warn(self, text: str | None) -> None:
        """
        For less serious, but still noteworthy problems.
        """
        if not text:
            return

        print(f"[{time.strftime('%H:%M:%S')}] {self.name}:WARNING: " + text)
        sys.stdout.flush()

    def error(self, text: str | None) -> None:
        """
        For critical bugs, usually followed by the program halting or the process restarting.
        """
        if not text:
            return

        print(f"[{time.strftime('%H:%M:%S')}] {self.name}:ERROR: " + text)
        sys.stdout.flush()