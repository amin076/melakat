from __future__ import annotations

import multiprocessing as mp
import sys

from PySide6.QtWidgets import QApplication

from .ui import MainWindow


def main() -> int:
    mp.freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
