import sys
import numpy as np
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QTableWidgetItem, QHBoxLayout, QTableWidget, QHeaderView, QScrollArea

# This function uses mathematical formulas obtained from the website below.
# Source: https://gall.dcinside.com/mgallery/board/view/?id=djmaxrespect&no=626587
# Please refer to the above link for more detailed information on the formula.
def calculate_power(x, c):
    if x < 90:
        t = 0.0
    elif x <= 94.5:
        t = (24 / 135 * np.exp(8 / 9 * (x - 95)) + 0.125)
    elif x <= 95:
        t = calculate_power(94.5, 1) + (calculate_power(95.5, 1) - calculate_power(94.5, 1)) * (x - 94.5) * (x - 94.5) * (x - 95.5) / 30
    elif x <= 95.5:
        t = (24 / 135 * np.exp(2 / 3 * (x - 95)) + 0.125)
    elif x < 96:
        t = calculate_power(96, 1) + 2 * (calculate_power(96.5, 1) - calculate_power(96, 1)) * (x - 96)
    elif x < 97.5:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (3 * x - 250.5) / 40
    elif x < 98:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (x - 76.5) / 20
    elif x < 98.5:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (3 * x - 186.5) / 100
    elif x < 99:
        t = (80 / 297 * (np.log(x - 95) - np.log(5)) + 10 / 11) * (x - 44) / 50
    elif x < 100:
        t = 8 / 27 * (np.log(x - 95) - np.log(5)) + 1
    elif x == 100:
        t = 1
    else:
        t = 0
    return t * c

# This constant value was obtained from a community website.
# Source: https://gall.dcinside.com/mgallery/board/view/?id=djmaxrespect&no=623125
difficulty_constant = {
    'SC15': 44,
    'SC14': 42,
    'SC13': 40,
    'SC12': 38,
    'SC11': 36,
    'SC10': 34,
    'SC9': 32,
    'SC8': 30,
    'SC7': 29,
    'SC6': 28,
    'SC5': 27,
    'SC4': 26,
    'SC3': 25,
    'SC2': 24,
    'SC1': 23,
    '15': 30,
    '14': 28,
    '13': 26,
    '12': 24,
    '11': 22,
    '10': 20,
    '9': 18,
    '8': 16,
    '7': 14,
    '6': 12,
    '5': 10,
    '4': 8,
    '3': 6,
    '2': 4,
    '1': 2
}

# 정확도별 power
results = {}
for difficulty, constant in difficulty_constant.items():
    for x in range(8500, 10001):
        accuracy = x / 100.0
        result = calculate_power(accuracy, constant * 2.22 + 2.31)
        if difficulty not in results:
            results[difficulty] = []
        results[difficulty].append((accuracy, result))

class PowerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        
        self.dj_power1_label = QLabel('가장 낮은 basic Dj Power:')
        input_layout.addWidget(self.dj_power1_label)
        
        self.dj_power1_input = QLineEdit(self)
        input_layout.addWidget(self.dj_power1_input)
        
        self.dj_power2_label = QLabel('가장 낮은 new Dj Power:')
        input_layout.addWidget(self.dj_power2_label)
        
        self.dj_power2_input = QLineEdit(self)
        input_layout.addWidget(self.dj_power2_input)
        
        main_layout.addLayout(input_layout)
        
        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate)
        main_layout.addWidget(self.calculate_button)
        
        results_layout = QHBoxLayout()
        
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        
        self.left_scroll = QScrollArea()
        self.right_scroll = QScrollArea()
        
        self.left_widget = QWidget()
        self.right_widget = QWidget()
        
        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)
        
        self.left_scroll.setWidget(self.left_widget)
        self.left_scroll.setWidgetResizable(True)
        self.right_scroll.setWidget(self.right_widget)
        self.right_scroll.setWidgetResizable(True)
        
        results_layout.addWidget(self.left_scroll)
        results_layout.addWidget(self.right_scroll)
        
        main_layout.addLayout(results_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('디제이맥스 DJ Power 갱신 계산기')
        self.setGeometry(300, 300, 800, 600)
        
        self.left_labels = {}
        self.right_labels = {}
        
        for i, key in enumerate(difficulty_constant.keys()):
            if i < 15:
                label = QLabel(f"{key} : -", self)
                self.left_layout.addWidget(label)
                self.left_labels[key] = label
            else:
                label = QLabel(f"{key} : -", self)
                self.right_layout.addWidget(label)
                self.right_labels[key] = label
        
    def calculate(self):
        dj_power1 = self.dj_power1_input.text()
        dj_power2 = self.dj_power2_input.text()
        
        for difficulty in difficulty_constant.keys():
            if dj_power1:
                try:
                    dj_power1_value = float(dj_power1)
                    accuracies1 = [acc for acc, power in results[difficulty] if power > dj_power1_value]
                    basic_acc = f"{min(accuracies1)}" if accuracies1 else "-"
                except ValueError:
                    basic_acc = "-"
            else:
                basic_acc = "-"
                
            if dj_power2:
                try:
                    dj_power2_value = float(dj_power2)
                    accuracies2 = [acc for acc, power in results[difficulty] if power > dj_power2_value]
                    new_acc = f"{min(accuracies2)}" if accuracies2 else "-"
                except ValueError:
                    new_acc = "-"
            else:
                new_acc = "-"
            
            if difficulty in self.left_labels:
                self.left_labels[difficulty].setText(f"{difficulty} :\t Basic: {basic_acc},\t New: {new_acc}")
            else:
                self.right_labels[difficulty].setText(f"{difficulty} :\t Basic: {basic_acc},\t New: {new_acc}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PowerApp()
    ex.show()
    sys.exit(app.exec_())