from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox


class astabKipp():
    
    def qtBox(self):

        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Betriebsspannung Vcc in V = "))
        self.VCC = QLineEdit()
        self.layout.addWidget(self.VCC)

        self.layout.addWidget(QLabel("Frequenz f in Hz = "))
        self.f = QLineEdit()
        self.layout.addWidget(self.f)

        self.layout.addWidget(QLabel("Verhältnis t1/t2 = "))
        self.V = QLineEdit()
        self.layout.addWidget(self.V)

        self.layout.addWidget(QLabel("CE-Strom der Transistoren in A = "))
        self.I = QLineEdit()
        self.layout.addWidget(self.I)


        self.button = QPushButton("Berrechnen \n")
        self.layout.addWidget(self.button)

        # Viele Label für die Ergebnisse, die in on_button_clicked mit setText() gefüllt werden
        self.RC12 = QLabel()
        self.layout.addWidget(self.RC12)
        self.RB12 = QLabel()
        self.layout.addWidget(self.RB12)
        self.C1 = QLabel()
        self.layout.addWidget(self.C1)
        self.C2 = QLabel()
        self.layout.addWidget(self.C2)

        def on_button_clicked():

            self.berrechnen(float(self.VCC.text()), float(self.f.text()), float(self.V.text()), float(self.I.text()) )

            self.RC12.setText("Rc1 und Rc2 = " + str( self.values["RC12"]) + "Ohm")
            self.RB12.setText("Rb1 und Rb2 = " + str( self.values["RB12"]) + "Ohm")
            self.C1.setText("C1 = " + self.smallFloatString( self.values["C1"]) + "F")
            self.C2.setText("C2 = " + self.smallFloatString( self.values["C2"]) + "F")


        self.button.clicked.connect(on_button_clicked)

        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()
        
    def berrechnen(self, VCC, f, V, I):
        
        # Rc1 und 2 mit dem CE-Strom berrechnen
        rc12 = VCC/I

        # Rb1 und Rb2 nach der Faustformel berrechnen
        rb12 = rc12 * 10

        # tau1 und tau2 berrechnen
        tau1 = 1 / ( f * ( 0.69 + 0.69 * 1/V ) )
        tau2 = 1 / ( f * ( 0.69 + 0.69 * V ) )

        # jeweils C mit tau und Rb berrechnen
        c1 = tau1 / rb12
        c2 = tau2 / rb12

        # errechnete Werte self.values zuweisen
        self.values["RC12"] = round(rc12)
        self.values["RB12"] = round(rb12)
        self.values["C1"] = c1
        self.values["C2"] = c2

    def smallFloatString(self, flt):
        
        fltString = str(flt)

        exponent = fltString[len(fltString) - 3]
        exponent += fltString[len(fltString) - 2]
        exponent += fltString[len(fltString) - 1]
        exponent = int(exponent)

        mantissa = fltString[0]
        mantissa += fltString[1]
        mantissa += fltString[2]
        mantissa += fltString[3]
        mantissa = float(mantissa)

        # this adds the correspondending SI prefix and scales the mantissa
        if exponent == -1:
            return str(round(mantissa * 100, 2)) + "m"
        if exponent == -2:
            return str(round(mantissa * 10, 2)) + "m"
        if exponent == -3:
            return str(round(mantissa * 1, 2)) + "m"
        if exponent == -4:
            return str(round(mantissa * 100, 2)) + "µ"
        if exponent == -5:
            return str(round(mantissa * 10, 2)) + "µ"
        if exponent == -6:
            return str(round(mantissa * 1, 2)) + "µ"
        if exponent == -7:
            return str(round(mantissa * 100, 2)) + "n"
        if exponent == -8:
            return str(round(mantissa * 10, 2)) + "n"
        if exponent == -9:
            return str(round(mantissa * 1, 2)) + "n"
        if exponent == -10:
            return str(round(mantissa * 100, 2)) + "p"
        if exponent == -11:
            return str(round(mantissa * 10, 2)) + "p"
        if exponent == -12:
            return str(round(mantissa * 1, 2)) + "p"

        # if the float is out of the supported range
        return str(flt)

    def __init__(self):

        self.values = {"RC12": 0, "RB12": 0,"C1": 0, "C2": 0}

        self.qtBox()
        

start = astabKipp()
