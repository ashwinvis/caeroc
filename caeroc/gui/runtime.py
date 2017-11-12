# -*- coding: utf-8 -*-
import sys
from caeroc import formulae
try:
    from PySide import QtCore
    from PySide.QtCore import Slot
    from PySide.QtGui import QDialog, QStandardItemModel, QApplication
    from caeroc.gui.base_pyside import Ui_CalcDialog
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtWidgets import QDialog
    from PyQt5.QtGui import QStandardItemModel
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
        self.key1 = self.ui.qcb1_input
        self.key2 = self.ui.qcb2_input
        self._default_values()
        # ---------Output------------
        self.table = self.ui.qtw_output
        self._setupModel()

    def _default_values(self):
        """Initialize scalar values which keep track of different options in
        the GUI.

        """
        self.input1 = 0.5
        self.input2 = 0.0
        self.gamma = 1.4
        self.autocalc = False
        self.mode = None
        self.on_qrb1_isen_pressed()

    def _setupModel(self):
        """Sets up the model or the table where the output is displayed."""
        self.model = QStandardItemModel(10, 2, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Parameter")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Value")

    def _set_mode_with_keys_and_attrs(self, key1_to_attr, key2_to_attr,
                                      extra_attr_to_key):
        """Reinitialize self.mode with an object of self.Mode - an alias for
        the formulae class. Also, clear the current options and add the related
        options for self.Mode.

        """
        if not isinstance(self.mode, self.Mode):
            self.mode = self.Mode(gamma=self.gamma)
            self.key1.clear()
            self.key2.clear()
            self.key1_to_attr = key1_to_attr
            self.key2_to_attr = key2_to_attr
            self._set_attr_to_key(extra_attr_to_key)
            self.key1.addItems(self.key1_to_attr.keys())
            self.key2.addItems(self.key2_to_attr.keys())
            print('MODE: {}'.format(self.mode.__doc__))

    def _set_attr_to_key(self, extra=None):
        self.attr_to_key = {v: k for k, v in self.key1_to_attr.items()}
        self.attr_to_key.update({v: k for k, v in self.key2_to_attr.items()})
        self.attr_to_key.update(extra)

    @Slot()
    def on_qrb1_isen_pressed(self):
        """Run when radio button is pressed."""
        self.Mode = formulae.isentropic.Isentropic
        key1_to_attr = {'M': 'M',
                        u'p/p\u2080': 'p_p0',
                        u'ρ/ρ\u2080': 'rho_rho0',
                        u'T/T\u2080': 'T_T0',
                        'A/A*': 'A_Astar'}
        key2_to_attr = {'-': None}
        extra_attr_to_key = {'Mt': 'M*',
                             'p_pt': 'p/p*',
                             'rho_rhot': u'ρ/ρ*',
                             'T_Tt': 'T/T*'}
        self._set_mode_with_keys_and_attrs(key1_to_attr, key2_to_attr,
                                           extra_attr_to_key)

    @Slot()
    def on_qrb2_expa_pressed(self):
        """Run when radio button is pressed."""
        self.Mode = formulae.isentropic.Expansion
        key1_to_attr = {u'θ (deg)': 'theta_deg',
                        u'θ (rad)': 'theta_rad'}
        key2_to_attr = {u'M\u2081': 'M_1',
                        u'ν\u2081 (rad)': 'nu_1'}
        extra_attr_to_key = {'theta': u'θ (rad)',
                             'M_2': u'M\u2082',
                             'nu_2': u'ν\u2082 (rad)',
                             'p2_p1': u'p\u2082/p\u2081',
                             'rho2_rho1': u'ρ\u2082/ρ\u2081',
                             'T2_T1': u'T\u2082/T\u2081'}
        self._set_mode_with_keys_and_attrs(key1_to_attr, key2_to_attr,
                                           extra_attr_to_key)

    @Slot(float)
    def on_qdsb1_input_valueChanged(self, value):
        """Run when input value in the QDoubleSpinBox changes."""
        self.input1 = value
        if self.autocalc:
            self.on_qpb_calculate_released()

    @Slot(float)
    def on_qdsb2_input_valueChanged(self, value):
        """Run when input value in the QDoubleSpinBox changes."""
        self.input2 = value
        if self.autocalc:
            self.on_qpb_calculate_released()

    @Slot(float)
    def on_qdsb_gamma_valueChanged(self, value):
        """Run when input value in the QDoubleSpinBox changes."""
        self.gamma = value
        del(self.mode)
        self.mode = self.Mode(gamma=value)
        if self.autocalc:
            self.on_qpb_calculate_released()

    @Slot()
    def on_qcb_autocalc_stateChanged(self):
        """Run when the QComboBox state changes."""
        self.autocalc = not self.autocalc
        print('Auto calculate: ', self.autocalc)

    @Slot()
    def on_qpb_calculate_released(self):
        """Run when the QPushButton is pressed and released."""
        attr1 = self.key1_to_attr[self.key1.currentText()]
        attr2 = self.key2_to_attr[self.key2.currentText()]
        if attr2 is None:
            kwargs = {attr1: self.input1}
        else:
            kwargs = {attr1: self.input1, attr2: self.input2}

        print(kwargs)
        self.mode.calculate(**kwargs)
        print(self.mode.data)

        # ------ Fill table --------------
        self.model.removeRows(0,
                              self.model.rowCount(QtCore.QModelIndex()),
                              QtCore.QModelIndex())
        row = 0
        for attr in self.mode.keys:
            if self.mode.data[attr]:  # Not empty
                self.model.insertRows(row, 1, QtCore.QModelIndex())
                self.model.setData(self.model.index(row, 0, QtCore.QModelIndex()),
                                   self.attr_to_key[attr])
                self.model.setData(self.model.index(row, 1, QtCore.QModelIndex()),
                                   str(self.mode.data[attr].pop()))
                row += 1
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalcDialog()
    calculator.show()
    sys.exit(app.exec_())
