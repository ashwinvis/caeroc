"""Provides class which connects formulae and data to UI elements through
Qt signals and slots.

"""
import sys
from qtpy import QtGui, QtCore, QtWidgets
from qtpy import PYQT4, PYQT5, PYSIDE, PYSIDE2

import pyqtgraph as pg
import numpy as np
from .. import formulae
from ..logger import logger
if PYQT4 or PYQT5:
    from .base_pyqt import Ui_CalcDialog
    logger.debug('Using PyQt5 backend.')
elif PYSIDE2:
    from .base_pyside2 import Ui_CalcDialog
    logger.debug('Using PySide2 backend.')
elif PYSIDE:
    from .base_pyside import Ui_CalcDialog
    logger.debug('Using PySide backend.')

Slot = QtCore.Slot


class CalcDialog(QtWidgets.QDialog):
    """
    Bridges all events in QApplication CalcApp to caeroc.formulae
    TODO: Error handling
    """
    def __init__(self, parent=None):
        """Initialize scalar values which keep track of different options in
        the GUI and setup the application user interface.

        """
        super(CalcDialog, self).__init__(parent)

        self.ui = Ui_CalcDialog()
        self.ui.setupUi(self)
        # ----------Input------------
        self.key1 = self.ui.qcb1_input
        self.key2 = self.ui.qcb2_input
        self.input1 = 1.0
        self.input2 = 1.0
        self.gamma = 1.4
        self.autocalc = False
        self.mode = None
        self.on_qrb1_isen_pressed()
        # ---------Output------------
        self.table = self.ui.qtw_output
        self._setupModel()

        # -----Connect Signals-------
        self.autocalc = False
        if PYQT4 or PYQT5:
            self.ui.qcb_autocalc.setChecked(self.autocalc)
            self.ui.qcb_autocalc.stateChanged.connect(
                self.on_qcb_autocalc_stateChanged)
            self.ui.qpb_plot.pressed.connect(
                self.on_qpb_pressed)

    def _setupModel(self):
        """Sets up the model or the table where the output is displayed."""
        self.model = QtGui.QStandardItemModel(10, 2, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Parameter")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Value")

    def _set_keys_and_attrs(self, key1_to_attr, key2_to_attr,
                            extra_attr_to_key, **kwargs):
        """Reinitialize self.mode with an object of self.Mode - an alias for
        the formulae class. Also, clear the current options and add the related
        options for self.Mode.

        """

        if not isinstance(self.mode, self.Mode):
            self.key1.clear()
            self.key2.clear()
            self.key1_to_attr = key1_to_attr
            self.key2_to_attr = key2_to_attr
            self._set_attr_to_key(extra_attr_to_key)

            keys1 = self.key1_to_attr.keys()
            keys2 = self.key2_to_attr.keys()
            if not (PYQT4 and PYQT5):
                keys1 = list(keys1)
                keys2 = list(keys2)

            self.key1.addItems(keys1)
            self.key2.addItems(keys2)

    def _set_mode(self, **kwargs):
        if not isinstance(self.mode, self.Mode):
            self.mode = self.Mode(gamma=self.gamma, **kwargs)
            logger.debug('MODE: {}'.format(self.mode.__doc__))

    def _set_attr_to_key(self, extra=None):
        self.attr_to_key = {v: k for k, v in self.key1_to_attr.items()}
        self.attr_to_key.update({v: k for k, v in self.key2_to_attr.items()})
        self.attr_to_key.update(extra)

    @Slot()
    def on_qpb_pressed(self):
        """run when plot buttong is pressed"""
        # PlotWindow(None)
        # x_min = self.mode.minima['M']
        x_min = 0.1
        x_max = self.mode.maxima['M']
        x_range = np.linspace(x_min, x_max, 500, endpoint=True)
        y = np.zeros_like(x_range)
        for index, val in enumerate(x_range):
            kwargs = {'M': val}
            self.mode.calculate(**kwargs)
            outcome = self.mode.data['p_p0'].pop()
            y[index] = outcome
        pg.plot(x_range, y)

    @Slot()
    def on_qrb1_isen_pressed(self):
        """Run when radio button Isentropic is pressed."""
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
        self._set_keys_and_attrs(key1_to_attr, key2_to_attr,
                                 extra_attr_to_key)
        self._set_mode()

    @Slot()
    def on_qrb2_expa_pressed(self):
        """Run when radio button Expansion is pressed."""
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
        self._set_keys_and_attrs(key1_to_attr, key2_to_attr,
                                 extra_attr_to_key)
        self._set_mode()

    @Slot()
    def on_qrb3_norm_pressed(self):
        """Run when radio button Normal Shock is pressed."""
        self.Mode = formulae.shock.NormalShock
        key1_to_attr = {u'M\u2081': 'M_1',
                        u'p\u2082/p\u2081': 'p2_p1',
                        u'ρ\u2082/ρ\u2080': 'rho2_rho1',
                        u'T\u2082/T\u2081': 'T2_T1'}
        key2_to_attr = {'-': None}
        extra_attr_to_key = {'M_2': u'M\u2082',
                             'p02_p01': u'p0\u2082/p0\u2081',
                             'rho02_rho01': u'ρ0\u2082/ρ0\u2080', 
                             'T02_T01': u'T0\u2082/T0\u2081'}

        self._set_keys_and_attrs(key1_to_attr, key2_to_attr,
                                 extra_attr_to_key)
        kwargs = dict()
        key1 = self.key1.currentText()
        attr1 = key1_to_attr[key1]
        kwargs[attr1] = self.input1
        self._set_mode(**kwargs)

    @Slot()
    def on_qrb4_obli_pressed(self):
        """Run when radio button Oblique Shock is pressed."""
        logger.warn('MODE:Oblique Shock not implemented')

    @Slot()
    def on_qrb5_fann_pressed(self):
        """Run when radio button Fanno Flow is pressed."""
        logger.warn('MODE:Fanno Flow not implemented')

    @Slot()
    def on_qrb6_rayl_pressed(self):
        """Run when radio button Rayleigh Flow is pressed."""
        logger.warn('MODE:Rayleigh Flow not implemented')

    @Slot(float)
    def on_qdsb1_input_valueChanged(self, value):
        """Run when input value in the 1st input QDoubleSpinBox changes."""
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
        """Run when the AutoCalculate QCheckBox state changes."""
        self.autocalc = self.ui.qcb_autocalc.isChecked()
        logger.debug('Auto calculate: {}'.format(self.autocalc))

    @Slot()
    def on_qpb_calculate_released(self):
        """Remove the rows and update the model with new data.
        Runs when the QPushButton is pressed and released.

        """
        attr1 = self.key1_to_attr[self.key1.currentText()]
        attr2 = self.key2_to_attr[self.key2.currentText()]
        if attr2 is None:
            kwargs = {attr1: self.input1}
        else:
            kwargs = {attr1: self.input1, attr2: self.input2}

        logger.info(kwargs)
        self.mode.calculate(**kwargs)
        logger.info(self.mode.data)

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
    app = QtWidgets.QApplication(sys.argv)
    calculator = CalcDialog()
    calculator.show()
    sys.exit(app.exec_())
