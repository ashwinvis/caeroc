import sys
from caeroc import formulae
try:
    from PySide import QtCore
    from PySide.QtCore import Slot
    from PySide.QtGui import QDialog, QStandardItemModel
    from caeroc.gui.base_pyside import Ui_CalcDialog
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtWidgets import QDialog, QStandardItemModel
    from caeroc.gui.base_pyqt import Ui_CalcDialog

class CalcDialog(QDialog):
    """
    Bridges all events in QApplication CalcApp to caeroc.formulae
    TODO: Error handling
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.ui = Ui_CalcDialog()
        self.ui.setupUi(self)
        # ----------Input------------
        self._default_values()
        # ---------Output------------
        self.table = self.ui.qtw_output
        self._setupModel()

    def _default_values(self):
        self.mode = formulae.isentropic.Isentropic()
        self.input1 = None
        self.input2 = None
        self.gamma = 1.4

    def _setupModel(self):
        self.model = QStandardItemModel(10, 2, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Parameter")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Value")
    
    @Slot()
    def on_qrb1_isen_pressed(self):
        self.mode = formulae.isentropic.Isentropic()
        print 'MODE: '+self.mode.__doc__

    @Slot(float)
    def on_qdsb1_input_valueChanged(self, value):
        self.input1 = value

    @Slot(float)
    def on_qdsb2_input_valueChanged(self, value):
        self.input2 = value

    @Slot(float)
    def on_qle_gamma_valueChanged():
        self.gamma = value
        print value

    @Slot()
    def on_qpb_calculate_released(self):
        self.key1 = 'M'
        self.key2 = None
        if self.key2 is None:
            kwargs = {self.key1:self.input1, 'gamma':self.gamma}
        else:
            kwargs = {self.key1:self.input1, self.key2:self.input2, 'gamma':self.gamma}

        self.mode.calculate(**kwargs)
        
        # ------ Fill table --------------
        self.model.removeRows(0,
                              self.model.rowCount(QtCore.QModelIndex()),
                              QtCore.QModelIndex())
        row = 0
        for k in self.mode.keys:
            if self.mode.data[k]: #Not empty
                self.model.insertRows(row, 1, QtCore.QModelIndex())
                self.model.setData(self.model.index(row, 0, QtCore.QModelIndex()),
                                    k)
                self.model.setData(self.model.index(row, 1, QtCore.QModelIndex()),
                                    self.mode.data[k].pop())
                row += 1

        self.table.setModel(self.model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalcDialog()
    calculator.show()
    sys.exit(app.exec_())
