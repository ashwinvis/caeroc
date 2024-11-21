import sys

from caeroc.gui import runtime

try:
    from PySide2.QtWidgets import QApplication as _QtApp
except ImportError:
    from PyQt5.QtWidgets import QApplication as _QtApp


class CalcApp:
    def __init__(self):
        try:
            self.app = _QtApp(sys.argv)
        except RuntimeError:
            self.app = _QtApp.instance()  # if QApplication already exists
        self.dialog = runtime.CalcDialog()

    def run(self):
        self.dialog.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    CalcApp().run()
