import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class QueryWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.resize(400, 300) # 设置界面大小
        self.setWindowTitle('查询界面')

        self.student_id_label = QLabel('学号:', self)
        self.student_name_label = QLabel('姓名:', self)

        self.student_id_input = QLineEdit(self)
        self.student_name_input = QLineEdit(self)

        self.return_button = QPushButton('返回主界面', self)
        self.query_button = QPushButton('查询', self)

        self.output_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.student_id_label)
        layout.addWidget(self.student_id_input)
        layout.addWidget(self.student_name_label)
        layout.addWidget(self.student_name_input)
        layout.addWidget(self.return_button)
        layout.addWidget(self.query_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.query_button.clicked.connect(self.query_student)

    def return_to_main_window(self):
        self.close()

    def query_student(self):
        student_id = self.student_id_input.text()
        student_name = self.student_name_input.text()

        result = f'学号: {student_id}, 姓名: {student_name}'
        self.output_label.setText(result)