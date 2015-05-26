import sys
from caeroc import formulae
from caeroc.gui import QDialog, QApplication, Ui_CalcDialog, Slot

class CalcDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.ui = Ui_CalcDialog()
        self.ui.setupUi(self)
    
    @Slot()
    def on_qrb1_isen_pressed(self):
        self.mode = formulae.isentropic.Isentropic
        print self.mode.__doc__

    @Slot(str)
    def on_qdsb1_input_valueFromText(self, value):
        self.input1 = value
        print value

    @Slot(int)
    def on_qdsb2_input_valueChanged(self, value):
        self.input2 = value
        print value

    @Slot(int)
    def on_qle_gamma_valueChanged():
        self.gamma = value
        print value
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalcDialog()
    calculator.show()
    sys.exit(app.exec_())
