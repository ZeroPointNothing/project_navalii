"""
Error handler for Navalii Browser.

Recieves the full exception through the --exception flag.
"""

import argparse
import tkinter as tk
import time
from tkinter import messagebox


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullexc", required=True, help="Full exception details as a string")
    parser.add_argument("--details", required=True, help="Short details.")
    return parser.parse_args()


def show_error_message(message, trc):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    messagebox.showerror("Error", message)

    # Get our line breaks back.
    trc = trc.replace("lnbrk", "\n")

    with open('traceback.txt', 'w') as f:
        f.write(f"[{time.ctime()}] Ouch!\n- - - - An exception occured: - - - -\n")
        f.write(trc)


if __name__ == "__main__":
    args = parse_arguments()
    traceback_str = args.fullexc

    print("Navalii shutdown unexpectedly. Check traceback.txt for more info.")
    show_error_message(f"Oh no! An error occurred!!\n\n{args.details}", traceback_str)
