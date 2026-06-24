from __future__ import annotations

import argparse

from .core.self_check import run_self_check
from .gui.main_window import run_gui
from .version import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="TecsoLetolto")
    parser.add_argument("--version", action="store_true", help="Print the application version.")
    parser.add_argument("--self-check", action="store_true", help="Run a portable runtime self-check.")
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    if args.self_check:
        result = run_self_check()
        for item in result.items:
            status = "OK" if item.ok else "FAIL"
            print(f"{status} {item.name}: {item.detail}")
        return 0 if result.ok else 1

    return run_gui()
