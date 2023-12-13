import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(400, 400)
        self.setWindowTitle('窗口布局示例')

        # 创建三个小框并水平排列
        boxes_layout = QHBoxLayout()

        # 标签
        box1 = QFrame(self)
        box1.setFrameShape(QFrame.Box)
        box1_layout = QVBoxLayout()
        label1 = QLabel('教师信息增删', self)
        label1.setAlignment(Qt.AlignHCenter)
        label_teacher_id = QLabel('Teacher ID:', self)
        label_rank = QLabel('Rank:', self)
        label_name = QLabel('Name:', self)
        label_research_id = QLabel('Research ID:', self)
        label_laboratory_id = QLabel('Laboratory ID:', self)
        label_faculty_id = QLabel('Faculty ID:', self)
        
        # 输入框
        input_teacher_id = QLineEdit(self)
        input_rank = QLineEdit(self)
        input_name = QLineEdit(self)
        input_research_id = QLineEdit(self)
        input_laboratory_id = QLineEdit(self)
        input_faculty_id = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box1_layout.addWidget(label1)
        box1_layout.addSpacing(20)
        box1_layout.addWidget(label_teacher_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(input_teacher_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_rank)
        box1_layout.addStretch(1)
        box1_layout.addWidget(input_rank)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_name)
        box1_layout.addStretch(1)
        box1_layout.addWidget(input_name)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_research_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(input_research_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_laboratory_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(input_laboratory_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_faculty_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(input_faculty_id)
        box1_layout.addStretch(20)
        
        # 按钮
        add_button_box1 = QPushButton('添加', self)
        delete_button_box1 = QPushButton('删除', self)
        buttons_layout_box1 = QHBoxLayout()
        buttons_layout_box1.addWidget(add_button_box1)
        buttons_layout_box1.addWidget(delete_button_box1)

        # 将按钮添加到布局
        box1_layout.addLayout(buttons_layout_box1)

        box1.setLayout(box1_layout)

        # 第二个框
        box2 = QFrame(self)
        box2.setFrameShape(QFrame.Box)
        box2_layout = QVBoxLayout()
        label2 = QLabel('论文信息增删', self)
        label2.setAlignment(Qt.AlignHCenter)
        label_doi = QLabel('DOI:', self)
        label_title = QLabel('Title:', self)
        label_author = QLabel('Author:', self)
        label_year = QLabel('Year:', self)
        
        # 添加对应的输入框
        input_doi = QLineEdit(self)
        input_title = QLineEdit(self)
        input_author = QLineEdit(self)
        input_year = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box2_layout.addWidget(label2)
        box2_layout.addSpacing(20)
        box2_layout.addWidget(label_doi)
        box2_layout.addStretch(1)
        box2_layout.addWidget(input_doi)
        box2_layout.addStretch(1)
        box2_layout.addWidget(label_title)
        box2_layout.addStretch(1)
        box2_layout.addWidget(input_title)
        box2_layout.addStretch(1)
        box2_layout.addWidget(label_author)
        box2_layout.addStretch(1)
        box2_layout.addWidget(input_author)
        box2_layout.addStretch(1)
        box2_layout.addWidget(label_year)
        box2_layout.addStretch(1)
        box2_layout.addWidget(input_year)
        box2_layout.addStretch(20)
        
        # 按钮
        add_button_box2 = QPushButton('添加', self)
        delete_button_box2 = QPushButton('删除', self)
        buttons_layout_box2 = QHBoxLayout()
        buttons_layout_box2.addWidget(add_button_box2)
        buttons_layout_box2.addWidget(delete_button_box2)

        # 将按钮添加到布局
        box2_layout.addLayout(buttons_layout_box2)

        box2.setLayout(box2_layout)

        # 第三个框
        box3 = QFrame(self)
        box3.setFrameShape(QFrame.Box)
        box3_layout = QVBoxLayout()
        label3 = QLabel('研究方向增删', self)
        label3.setAlignment(Qt.AlignHCenter)
        label_research_id_3 = QLabel('Research ID:', self)
        label_name_3 = QLabel('Name:', self)
        
        # 添加对应的输入框
        input_research_id_3 = QLineEdit(self)
        input_name_3 = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box3_layout.addWidget(label3)
        box3_layout.addSpacing(20)
        box3_layout.addWidget(label_research_id_3)
        box3_layout.addStretch(1)
        box3_layout.addWidget(input_research_id_3)
        box3_layout.addStretch(1)
        box3_layout.addWidget(label_name_3)
        box3_layout.addStretch(1)
        box3_layout.addWidget(input_name_3)
        box3_layout.addStretch(20)
        
        box3.setLayout(box3_layout)

        # 将三个小框添加到水平布局中
        boxes_layout.addWidget(box1)
        boxes_layout.addWidget(box2)
        boxes_layout.addWidget(box3)

        # 按钮
        add_button_box3 = QPushButton('添加', self)
        delete_button_box3 = QPushButton('删除', self)
        buttons_layout_box3 = QHBoxLayout()
        buttons_layout_box3.addWidget(add_button_box3)
        buttons_layout_box3.addWidget(delete_button_box3)

        # 将按钮添加到布局
        box3_layout.addLayout(buttons_layout_box3)

        self.setLayout(boxes_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
