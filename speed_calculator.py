from PyQt6.QtWidgets import (QApplication,QLabel ,QWidget ,
        QGridLayout ,QLineEdit , QPushButton,QComboBox)

import sys

class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speed Calculator ")
        grid = QGridLayout()

        time_label  = QLabel("Time : ")
        self.time_input = QLineEdit()

        distance_label = QLabel("Distance : ")
        self.distance_input = QLineEdit()

        combo_label = QLabel("Metric ")
        self.combo = QComboBox()
        self.combo.addItems(['Miles', 'Kilo Meters'])


        calculate_button = QPushButton("Calculate Speed")
        calculate_button.clicked.connect(self.calculate)
        self.output_label = QLabel("")

        grid.addWidget(time_label,1,0)
        grid.addWidget(self.time_input,1,1)
        grid.addWidget(distance_label,0,0)
        grid.addWidget(self.distance_input,0,1)
        grid.addWidget(combo_label,2,0)
        grid.addWidget(self.combo,2,1)
        grid.addWidget(calculate_button,3,0,2,2)
        grid.addWidget(self.output_label,4,0,2,2)

        self.setLayout(grid)

    def calculate(self):
        if self.combo.currentText() == 'Miles':
            distance = self.distance_input.text()
            time = self.time_input.text()
            speed = float(distance) / float(time)
            miles = "Miles per hour"
            self.output_label.setText(f"The speed is : {speed} {miles}")
        if self.combo.currentText() == 'Kilo Meters':
            distance = self.distance_input.text()
            time = self.time_input.text()
            speed = float(distance) / float(time)
            km = "Kilo Meters per hour"
            self.output_label.setText(f"The speed is : {speed} {km}")


app = QApplication(sys.argv)
speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())
