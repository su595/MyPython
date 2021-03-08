from PyQt5.QtCore import QLine
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class platz():


    def platzhalter(self):
        
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # jeweils ein Label und ein Eingabefeld (LineEdit) für Email und Password
        self.layout.addWidget(QLabel("Email: "))
        self.emailLE = QLineEdit()
        self.layout.addWidget(self.emailLE)
        self.layout.addWidget(QLabel("Password: "))
        self.pwLE = QLineEdit()
        self.layout.addWidget(self.pwLE)
        # und ein Login Knopf
        self.button = QPushButton("Login!")
        self.layout.addWidget(self.button)

        def on_button_clicked():
            # Wenn der Button gedrückt wird, wird das sichtbare Fenster geschlossen, der Code läuft normal weiter
            self.app.quit()
        
        self.button.clicked.connect(on_button_clicked)

        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

        return list((self.emailLE.text(), self.pwLE.text()))

abc = platz()

test = abc.platzhalter()

print(test)

