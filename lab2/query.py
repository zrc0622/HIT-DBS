import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox, QRadioButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
import pymysql

class QueryWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.resize(600, 400)
        self.setWindowTitle('查询界面')

        # 创建三个小框并水平排列
        boxes_layout = QHBoxLayout()

        # 提供教师姓名，查找该教师发表的文章（连接查询：paper、teacher）
        # 标签
        box1 = QFrame(self)
        box1.setFrameShape(QFrame.Box) # 边框
        box1_layout = QVBoxLayout() # 垂直排列
        label1 = QLabel('教师论文查询', self)
        label1.setAlignment(Qt.AlignHCenter)
        label1_teacher_name = QLabel('教师姓名:', self)
        
        # 输入框
        self.input_teacher_name = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box1_layout.addWidget(label1)
        box1_layout.addSpacing(40)
        box1_layout.addWidget(label1_teacher_name)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_teacher_name)
        box1_layout.addStretch(20)
        
        # 按钮
        add_button_box1 = QPushButton('查询', self)
        add_button_box1.clicked.connect(self.query1)

        # 将按钮添加到布局
        box1_layout.addWidget(add_button_box1)

        box1.setLayout(box1_layout)

        # 提供中心名称，查询该中心下的老师信息（嵌套查询：内嵌套laboratory，外嵌套teacher）
        # 第二个框
        box2 = QFrame(self)
        box2.setFrameShape(QFrame.Box)
        box2_layout = QVBoxLayout()
        label2 = QLabel('中心教师信息查询', self)
        label2.setAlignment(Qt.AlignHCenter)
        label_laboratory = QLabel('中心名:', self)
        
        # 添加对应的输入框
        self.input_laboratory_name = QComboBox(self)
        
        # 添加选项到下拉框
        self.input_laboratory_name.addItem('模式识别与智能系统研究中心')
        self.input_laboratory_name.addItem('机器人技术与系统研究中心')
        self.input_laboratory_name.addItem('智能接口与人机交互研究中心')
        self.input_laboratory_name.addItem('机器学习研究中心')
        
        # 将标签和输入框添加到布局中
        box2_layout.addWidget(label2)
        box2_layout.addSpacing(40)
        box2_layout.addWidget(label_laboratory)
        box2_layout.addStretch(1)
        box2_layout.addWidget(self.input_laboratory_name)
        box2_layout.addStretch(20)
        
        # 按钮
        add_button_box2 = QPushButton('查询', self)
        # add_button_box2.clicked.connect(self.add_to_paper)

        # 将按钮添加到布局
        box2_layout.addWidget(add_button_box2)

        box2.setLayout(box2_layout)

        # 输入年份，查询该年份老师发表论文数目（分组查询）
        # 第三个框
        box3 = QFrame(self)
        box3.setFrameShape(QFrame.Box)
        box3_layout = QVBoxLayout()
        label3 = QLabel('论文数量查询', self)
        label3.setAlignment(Qt.AlignHCenter)
        label_year = QLabel('年份:', self)
        
        # 添加对应的输入框
        self.input_year = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box3_layout.addWidget(label3)
        box3_layout.addSpacing(40)
        box3_layout.addWidget(label_year)
        box3_layout.addStretch(1)
        box3_layout.addWidget(self.input_year)
        box3_layout.addStretch(20)
        
        box3.setLayout(box3_layout)

        # 将三个小框添加到水平布局中
        boxes_layout.addWidget(box1)
        boxes_layout.addWidget(box2)
        boxes_layout.addWidget(box3)

        # 按钮
        add_button_box3 = QPushButton('添加', self)
        # add_button_box3.clicked.connect(self.add_to_research)

        # 将按钮添加到布局
        box3_layout.addWidget(add_button_box3)

        self.setLayout(boxes_layout)

    def query1(self): 
        teacher_name = self.input_teacher_name.text().strip() if self.input_teacher_name.text().strip() else None

        # 替换这些值为你的数据库连接详情
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'dbs_lab2'

        # 建立到数据库的连接
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            # 创建一个游标对象
            with connection.cursor() as cursor:
                # 执行查询操作
                sql_query = 'SELECT teacher.teacher_id, teacher.name, paper.title, paper.year FROM teacher, paper WHERE teacher.name = %s AND teacher.teacher_id=paper.author_id'
                cursor.execute(sql_query, (teacher_name))

            # 获取查询结果集
            result = cursor.fetchall()

            # 创建查询结果窗口并显示
            if result:
                query_result_dialog = QueryResultDialog(result)
                query_result_dialog.exec_()
            if not result:
                QMessageBox.warning(self, '警告', '没有查询到相关老师')

        except Exception as e:
            if e.args[0] == 1062:
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入重复值错误：可能是主键冲突')
            elif e.args[0] == 1048:
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入空值错误')
            elif e.args[0] == 1452:
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '外键约束错误')
            else: 
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()

# 查询结果表格
class QueryResultDialog(QDialog):
    def __init__(self, result):
        super().__init__()

        self.setWindowTitle('查询结果')
        self.resize(600, 400)

        if not result:
            return

        # 获取查询结果的列名
        column_headers = list(result[0].keys())

        # 创建一个表格
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(len(column_headers))  # 设置列数
        self.table_widget.setRowCount(len(result))  # 设置行数

        # 设置列标题
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        # 填充表格
        for row_idx, row_dict in enumerate(result):
            for col_idx, col_name in enumerate(column_headers):
                item = QTableWidgetItem('  '+str(row_dict.get(col_name, ''))+'  ')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # 居中对齐
                self.table_widget.setItem(row_idx, col_idx, item)

        # 设置列宽度自适应
        self.table_widget.resizeColumnsToContents()

        # 创建一个布局，将表格添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        # 创建一个按钮
        close_button = QPushButton('关闭', self)
        close_button.clicked.connect(self.close)

        # 将按钮添加到布局中
        layout.addWidget(close_button)

        # 设置布局
        self.setLayout(layout)