from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class FriendlyPython():
    

    def QtBox(self):

        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # jetzt wird dem Layout verschiedene Widgets hinzugefügt, wie LineEdits, Labels über den LineEdits und ein Button
        self.layout.addWidget(QLabel("Anzahl: "))
        self.zahl = QLineEdit()
        self.layout.addWidget(self.zahl)

        self.layout.addWidget(QLabel("Namen: "))
        self.name = QLineEdit()
        self.layout.addWidget(self.name)

        self.button = QPushButton("Begrüßen")
        self.layout.addWidget(self.button)

        # Die Funktion, die beim Klicken auf den Button ausgeführt wird
        def on_button_clicked():
            
            i = int(self.zahl.text())
            halloStr = ""

            # i-mal Hallo Name zum halloStr hinzufügen
            while i > 0:
                halloStr += "  Hallo " + self.name.text()
                # bei i-- meckert er irgendwie?!?!? 
                i = i - 1
            
            print(halloStr)

        self.button.clicked.connect(on_button_clicked)


        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()


myPython = FriendlyPython()
myPython.QtBox()