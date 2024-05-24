import sys
import pandas as pd

from CalculateModule import calculate_power
from const import difficulty_constant
from SongModule import load_dataframe, filter_songs

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QTableWidgetItem, QHBoxLayout, QTableWidget, QHeaderView, QScrollArea, QRadioButton, QListWidget, QSpacerItem, QSizePolicy

results = {}
for difficulty, constant in difficulty_constant.items():
    for x in range(8500, 10001):
        accuracy = x / 100.0
        result = calculate_power(accuracy, constant * 2.22 + 2.31)
        if difficulty not in results:
            results[difficulty] = []
        results[difficulty].append((accuracy, result))

songs_df = load_dataframe('DJMAX RESPECT V 2.0 _ Pattern Data.xlsx')
DLC_KEY = 'DLC_Unnamed: 1_level_1'
SONGNAME_KEY = '곡명_Unnamed: 2_level_1'

class PowerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        main_layout = QVBoxLayout()

        # 입력부
        input_layout = QVBoxLayout()

        # basic field
        basic_layout = QHBoxLayout()
        self.dj_power1_label = QLabel('가장 낮은 basic Dj Power:')
        self.dj_power1_input = QLineEdit(self)
        self.dj_power1_input.setFixedWidth(200)  # 입력 필드의 가로 길이를 조정
        basic_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        basic_layout.addWidget(self.dj_power1_label)
        basic_layout.addWidget(self.dj_power1_input)
        input_layout.addLayout(basic_layout)

        # new field
        new_layout = QHBoxLayout()
        self.dj_power2_label = QLabel('가장 낮은 new Dj Power:')
        self.dj_power2_input = QLineEdit(self)
        self.dj_power2_input.setFixedWidth(200)  # 입력 필드의 가로 길이를 조정
        new_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        new_layout.addWidget(self.dj_power2_label)
        new_layout.addWidget(self.dj_power2_input)
        input_layout.addLayout(new_layout)

        # 버튼 배치
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate)
        self.calculate_button.setFixedSize(100, 50)

        button_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.calculate_button)
        input_layout.addLayout(button_layout)

        main_layout.addLayout(input_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)) # 왼쪽 공간 확보

        # 달성 목표 정확도 목록
        results_layout = QHBoxLayout()
        
        self.sc_layout = QVBoxLayout() #sc
        self.nhm_layout = QVBoxLayout() # 그냥 레벨
        
        self.left_scroll = QScrollArea()
        self.middle_scroll = QScrollArea()
        
        self.left_widget = QWidget()
        self.middle_widget = QWidget()
        
        self.left_widget.setLayout(self.sc_layout)
        self.middle_widget.setLayout(self.nhm_layout)
        
        self.left_scroll.setWidget(self.left_widget)
        self.left_scroll.setWidgetResizable(True)
        self.middle_scroll.setWidget(self.middle_widget)
        self.middle_scroll.setWidgetResizable(True)
        
        results_layout.addWidget(self.left_scroll)
        results_layout.addWidget(self.middle_scroll)
        
        # 버튼 선택
        self.recommend_layout = QVBoxLayout()

        self.button_radio_row = QHBoxLayout()

        self.b4 = QRadioButton("4B")
        self.b5 = QRadioButton("5B")
        self.b6 = QRadioButton("6B")
        self.b8 = QRadioButton("8B")
        
        self.b4.setChecked(True) # 4버튼 기본

        self.button_radio_row.addWidget(self.b4)
        self.button_radio_row.addWidget(self.b5)
        self.button_radio_row.addWidget(self.b6)
        self.button_radio_row.addWidget(self.b8)

        self.recommend_layout.addLayout(self.button_radio_row)  # 가로 레이아웃을 세로 레이아웃에 추가

        # 추천 곡 목록
        self.recommend_list = QListWidget()
        self.recommend_layout.addWidget(self.recommend_list)
        
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.recommend_layout)
        self.right_scroll = QScrollArea()
        self.right_scroll.setWidget(self.right_widget)
        self.right_scroll.setWidgetResizable(True)
        
        results_layout.addWidget(self.right_scroll)
        
        main_layout.addLayout(results_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('디제이맥스 DJ Power 갱신 계산기')
        self.setGeometry(300, 300, 1200, 600)
        
        self.left_labels = {}
        self.middle_labels = {}
        
        for i, key in enumerate(difficulty_constant.keys()):
            if i < 15:
                label = QLabel(f"{key} : -", self)
                self.sc_layout.addWidget(label)
                self.left_labels[key] = label
            else:
                label = QLabel(f"{key} : -", self)
                self.nhm_layout.addWidget(label)
                self.middle_labels[key] = label
        
    def calculate(self):
        dj_power1 = self.dj_power1_input.text()
        dj_power2 = self.dj_power2_input.text()
        
        self.recommend_list.clear()
        
        recommand_songs = []
        
        for difficulty in difficulty_constant.keys():
            is_sc = False
            try:
                int(difficulty)
            except ValueError:
                is_sc = True
                
                
            if dj_power1:
                try:
                    dj_power1_value = float(dj_power1)
                    accuracies1 = [acc for acc, power in results[difficulty] if power > dj_power1_value]
                    
                    if accuracies1:
                        basic_acc = f"{min(accuracies1)}"
                        
                        if is_sc:
                            difficult = difficulty[2:]
                        songs = filter_songs(songs_df, 4, int(difficult), is_sc)
                        
                        for song in songs.iterrows():
                            recommand_songs.append((difficulty, song[1][SONGNAME_KEY], song[1][DLC_KEY]))
                            
                    else:
                        basic_acc = "-"
                        
                except ValueError:
                    basic_acc = "-"
            else:
                basic_acc = "-"
                
            if dj_power2:
                try:
                    dj_power2_value = float(dj_power2)
                    accuracies2 = [acc for acc, power in results[difficulty] if power > dj_power2_value]
                    
                    if accuracies2:
                        new_acc = f"{min(accuracies2)}"
                        
                        if is_sc:
                            difficult = difficulty[2:]
                        songs = filter_songs(songs_df, 4, int(difficult), is_sc)
                        
                        for song in songs.iterrows():
                            recommand_songs.append((difficulty, song[1][SONGNAME_KEY], song[1][DLC_KEY]))
                    else:
                        new_acc = "-"
                        
                except ValueError:
                    new_acc = "-"
            else:
                new_acc = "-"
            
            recommand_songs.sort(reverse=True)
            
            if difficulty in self.left_labels:
                self.left_labels[difficulty].setText(f"{difficulty} :\t Basic: {basic_acc},\t New: {new_acc}")
            else:
                self.middle_labels[difficulty].setText(f"{difficulty} :\t Basic: {basic_acc},\t New: {new_acc}")
                
        for song in recommand_songs:
            self.recommend_list.addItem(f"{song[0]}\t{song[1]}\t\t{song[2]}")
        
if __name__ == '__main__':
    # 정확도별 power
    app = QApplication(sys.argv)
    ex = PowerApp()
    ex.show()
    sys.exit(app.exec_())
