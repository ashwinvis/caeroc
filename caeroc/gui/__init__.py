import sys
try:
    from PySide.QtCore import Slot
    from PySide.QtGui import QDialog, QApplication
    from caeroc.gui.base_pyside import Ui_CalcDialog
except ImportError:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtWidgets import QDialog, QApplication
    from caeroc.gui.base_pyqt import Ui_CalcDialog

from caeroc.gui.runtime import CalcDialog

class CalcApp:
    def __init__(self):
        try:
            self.app = QApplication(sys.argv)
        except RuntimeError:
            self.app = QApplication.instance() # if QApplication already exists 
        self.dialog = CalcDialog()
        
    def run(self):
	self.dialog.show()
	sys.exit(self.app.exec_())


if __name__ == "__main__":
    CalcApp().run()
