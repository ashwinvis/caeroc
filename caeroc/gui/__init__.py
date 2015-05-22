import sys
from PySide import QtCore, QtGui

from caeroc.gui.base import Ui_Calc


class Calc_Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.ui = Ui_Calc()

        self.ui.setupUi(self)

    @QtCore.Slot(int)
    def on_inputSpinBox1_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox2.value()))

    @QtCore.Slot(int)
    def on_inputSpinBox2_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox1.value()))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    calculator = Calc_Dialog()
    calculator.show()
    sys.exit(app.exec_())
