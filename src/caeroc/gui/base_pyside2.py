################################################################################
## Form generated from reading UI file 'base.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CalcDialog:
    def setupUi(self, CalcDialog):
        if not CalcDialog.objectName():
            CalcDialog.setObjectName("CalcDialog")
        CalcDialog.resize(459, 692)
        self.verticalLayout_2 = QVBoxLayout(CalcDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridWidget = QWidget(CalcDialog)
        self.gridWidget.setObjectName("gridWidget")
        self.verticalLayout = QVBoxLayout(self.gridWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.valueFrame = QFrame(self.gridWidget)
        self.valueFrame.setObjectName("valueFrame")
        self.gridLayout = QGridLayout(self.valueFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.modeFrame = QFrame(self.valueFrame)
        self.modeFrame.setObjectName("modeFrame")
        self.gridLayout_2 = QGridLayout(self.modeFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.qrb4_obli = QRadioButton(self.modeFrame)
        self.qrb4_obli.setObjectName("qrb4_obli")

        self.gridLayout_2.addWidget(self.qrb4_obli, 3, 2, 1, 1)

        self.qrb3_norm = QRadioButton(self.modeFrame)
        self.qrb3_norm.setObjectName("qrb3_norm")

        self.gridLayout_2.addWidget(self.qrb3_norm, 2, 2, 1, 1)

        self.qrb1_isen = QRadioButton(self.modeFrame)
        self.qrb1_isen.setObjectName("qrb1_isen")
        self.qrb1_isen.setChecked(True)

        self.gridLayout_2.addWidget(self.qrb1_isen, 2, 1, 1, 1)

        self.qrb5_fann = QRadioButton(self.modeFrame)
        self.qrb5_fann.setObjectName("qrb5_fann")

        self.gridLayout_2.addWidget(self.qrb5_fann, 2, 3, 1, 1)

        self.qrb6_rayl = QRadioButton(self.modeFrame)
        self.qrb6_rayl.setObjectName("qrb6_rayl")

        self.gridLayout_2.addWidget(self.qrb6_rayl, 3, 3, 1, 1)

        self.label = QLabel(self.modeFrame)
        self.label.setObjectName("label")
        self.label.setEnabled(False)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 2, 0, 2, 1)

        self.qrb2_expa = QRadioButton(self.modeFrame)
        self.qrb2_expa.setObjectName("qrb2_expa")
        font1 = QFont()
        font1.setStrikeOut(False)
        self.qrb2_expa.setFont(font1)

        self.gridLayout_2.addWidget(self.qrb2_expa, 3, 1, 1, 1)

        self.gridLayout.addWidget(self.modeFrame, 0, 0, 1, 2)

        self.inputFrame = QFrame(self.valueFrame)
        self.inputFrame.setObjectName("inputFrame")
        self.gridLayout_3 = QGridLayout(self.inputFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.qcb1_input = QComboBox(self.inputFrame)
        self.qcb1_input.setObjectName("qcb1_input")

        self.gridLayout_3.addWidget(self.qcb1_input, 5, 3, 1, 1)

        self.formFrame = QFrame(self.inputFrame)
        self.formFrame.setObjectName("formFrame")
        self.formLayout = QFormLayout(self.formFrame)
        self.formLayout.setObjectName("formLayout")
        self.qcb_autocalc = QCheckBox(self.formFrame)
        self.qcb_autocalc.setObjectName("qcb_autocalc")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.qcb_autocalc)

        self.qpb_calculate = QPushButton(self.formFrame)
        self.qpb_calculate.setObjectName("qpb_calculate")
        self.qpb_calculate.setLayoutDirection(Qt.LeftToRight)
        self.qpb_calculate.setAutoFillBackground(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.qpb_calculate)

        self.gridLayout_3.addWidget(self.formFrame, 7, 4, 1, 1)

        self.label_3 = QLabel(self.inputFrame)
        self.label_3.setObjectName("label_3")
        self.label_3.setEnabled(False)
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setWeight(75)
        self.label_3.setFont(font2)

        self.gridLayout_3.addWidget(self.label_3, 5, 0, 2, 1)

        self.qdsb2_input = QDoubleSpinBox(self.inputFrame)
        self.qdsb2_input.setObjectName("qdsb2_input")
        self.qdsb2_input.setDecimals(8)
        self.qdsb2_input.setMinimum(-99.000000000000000)
        self.qdsb2_input.setSingleStep(0.100000000000000)
        self.qdsb2_input.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.qdsb2_input, 6, 4, 1, 1)

        self.qcb2_input = QComboBox(self.inputFrame)
        self.qcb2_input.setObjectName("qcb2_input")

        self.gridLayout_3.addWidget(self.qcb2_input, 6, 3, 1, 1)

        self.qdsb1_input = QDoubleSpinBox(self.inputFrame)
        self.qdsb1_input.setObjectName("qdsb1_input")
        self.qdsb1_input.setDecimals(8)
        self.qdsb1_input.setMaximum(999.990000000000009)
        self.qdsb1_input.setSingleStep(0.100000000000000)
        self.qdsb1_input.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.qdsb1_input, 5, 4, 1, 1)

        self.qdsb_gamma = QDoubleSpinBox(self.inputFrame)
        self.qdsb_gamma.setObjectName("qdsb_gamma")
        self.qdsb_gamma.setSingleStep(0.100000000000000)
        self.qdsb_gamma.setValue(1.400000000000000)

        self.gridLayout_3.addWidget(self.qdsb_gamma, 7, 3, 1, 1)

        self.label_2 = QLabel(self.inputFrame)
        self.label_2.setObjectName("label_2")
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 7, 0, 1, 1)

        self.gridLayout.addWidget(self.inputFrame, 2, 0, 4, 2)

        self.verticalLayout.addWidget(self.valueFrame)

        self.outputLayout = QGridLayout()
        self.outputLayout.setObjectName("outputLayout")
        self.label_4 = QLabel(self.gridWidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setEnabled(False)
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setWeight(75)
        font3.setKerning(True)
        self.label_4.setFont(font3)
        self.label_4.setAcceptDrops(False)

        self.outputLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.qtw_output = QTableView(self.gridWidget)
        self.qtw_output.setObjectName("qtw_output")
        self.qtw_output.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qtw_output.sizePolicy().hasHeightForWidth())
        self.qtw_output.setSizePolicy(sizePolicy)
        self.qtw_output.setAutoFillBackground(False)
        self.qtw_output.setFrameShape(QFrame.Box)
        self.qtw_output.setFrameShadow(QFrame.Plain)
        self.qtw_output.horizontalHeader().setCascadingSectionResizes(False)

        self.outputLayout.addWidget(self.qtw_output, 1, 0, 1, 1)

        self.verticalLayout.addLayout(self.outputLayout)

        self.buttonBox = QDialogButtonBox(self.gridWidget)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Close | QDialogButtonBox.Reset
        )

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout_2.addWidget(self.gridWidget)

        self.retranslateUi(CalcDialog)
        self.buttonBox.accepted.connect(CalcDialog.accept)
        self.buttonBox.rejected.connect(CalcDialog.reject)

        QMetaObject.connectSlotsByName(CalcDialog)

    # setupUi

    def retranslateUi(self, CalcDialog):
        CalcDialog.setWindowTitle(
            QCoreApplication.translate("CalcDialog", "Caeroc Calculator", None)
        )
        # if QT_CONFIG(tooltip)
        CalcDialog.setToolTip(
            QCoreApplication.translate(
                "CalcDialog", "<html><head/><body><p>Input</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.qrb4_obli.setText(
            QCoreApplication.translate("CalcDialog", "Ob&lique Shock", None)
        )
        self.qrb3_norm.setText(
            QCoreApplication.translate("CalcDialog", "&Normal Shock", None)
        )
        self.qrb1_isen.setText(
            QCoreApplication.translate("CalcDialog", "Isen&tropic", None)
        )
        self.qrb5_fann.setText(
            QCoreApplication.translate("CalcDialog", "Fanno F&low", None)
        )
        self.qrb6_rayl.setText(
            QCoreApplication.translate("CalcDialog", "Ra&yleigh Flow", None)
        )
        # if QT_CONFIG(tooltip)
        self.label.setToolTip(
            QCoreApplication.translate("CalcDialog", "Choose a formula set", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("CalcDialog", "Mode", None))
        self.qrb2_expa.setText(
            QCoreApplication.translate("CalcDialog", "E&xpansion", None)
        )
        self.qcb_autocalc.setText(
            QCoreApplication.translate("CalcDialog", "AutoCalculate", None)
        )
        self.qpb_calculate.setText(
            QCoreApplication.translate("CalcDialog", "Calculate", None)
        )
        self.label_3.setText(QCoreApplication.translate("CalcDialog", "Input", None))
        self.label_2.setText(QCoreApplication.translate("CalcDialog", "\u0263 =", None))
        # if QT_CONFIG(tooltip)
        self.label_4.setToolTip(
            QCoreApplication.translate("CalcDialog", "Tabulated output", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("CalcDialog", "Result", None))

    # retranslateUi
