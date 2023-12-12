import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from query import QueryWindow
from modify import ModifyWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__() # 调用父类初始化
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('教学管理系统')

        # 组件
        label = QLabel('教学管理系统', self)
        self.modify_button = QPushButton('修改', self) # 修改界面
        self.query_button = QPushButton('查询', self) # 查询界面

        layout = QVBoxLayout() # 设置垂直布局
        layout.addStretch(1) # 添加弹簧(参数表示比例)
        layout.addWidget(label)
        layout.addStretch(2)
        layout.addWidget(self.modify_button)
        layout.addStretch(1)
        layout.addWidget(self.query_button)
        layout.addStretch(2)

        self.setLayout(layout) # 将垂直布局添加到主窗口

        self.modify_button.clicked.connect(self.show_modify_window) # 连接修改按钮
        self.query_button.clicked.connect(self.show_query_window) # 连接查询按钮

        # 界面美化
        self.resize(600, 400) # 设置界面大小  
        self.modify_button.setFixedWidth(200) # 按钮长度  
        self.query_button.setFixedWidth(200) 
        layout.setAlignment(Qt.AlignHCenter) # 水平居中
        label.setAlignment(Qt.AlignHCenter)

    def show_query_window(self):
        self.query_window = QueryWindow(self)
        self.query_window.show()

    def show_modify_window(self):
        self.modify_window = ModifyWindow(self)
        self.modify_window.show()



if __name__ == '__main__':
    app = QApplication(sys.argv) # 创建QApplication对象，输入参数为运行程序时输入的命令行参数，相当于创建了初始界面
    main_window = MainWindow() # 创建主窗口对象
    main_window.show() # 显示主窗口
    sys.exit(app.exec_()) # 循环等待界面结束
