import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import pymysql

class ModifyWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.resize(600, 400)
        self.setWindowTitle('修改界面')

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
        self.input_teacher_id = QLineEdit(self)
        self.input_rank = QLineEdit(self)
        self.input_name = QLineEdit(self)
        self.input_research_id = QLineEdit(self)
        self.input_laboratory_id = QLineEdit(self)
        self.input_faculty_id = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box1_layout.addWidget(label1)
        box1_layout.addSpacing(20)
        box1_layout.addWidget(label_teacher_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_teacher_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_rank)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_rank)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_name)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_name)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_research_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_research_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_laboratory_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_laboratory_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(label_faculty_id)
        box1_layout.addStretch(1)
        box1_layout.addWidget(self.input_faculty_id)
        box1_layout.addStretch(20)
        
        # 按钮
        add_button_box1 = QPushButton('添加', self)
        add_button_box1.clicked.connect(self.add_to_teacher)
        delete_button_box1 = QPushButton('删除', self)
        delete_button_box1.clicked.connect(self.delete_from_teacher)
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
        self.input_doi = QLineEdit(self)
        self.input_title = QLineEdit(self)
        self.input_author = QLineEdit(self)
        self.input_year = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box2_layout.addWidget(label2)
        box2_layout.addSpacing(20)
        box2_layout.addWidget(label_doi)
        box2_layout.addStretch(1)
        box2_layout.addWidget(self.input_doi)
        box2_layout.addStretch(1)
        box2_layout.addWidget(label_title)
        box2_layout.addStretch(1)
        box2_layout.addWidget(self.input_title)
        box2_layout.addStretch(1)
        box2_layout.addWidget(label_author)
        box2_layout.addStretch(1)
        box2_layout.addWidget(self.input_author)
        box2_layout.addStretch(1)
        box2_layout.addWidget(label_year)
        box2_layout.addStretch(1)
        box2_layout.addWidget(self.input_year)
        box2_layout.addStretch(20)
        
        # 按钮
        add_button_box2 = QPushButton('添加', self)
        add_button_box2.clicked.connect(self.add_to_paper)
        delete_button_box2 = QPushButton('删除', self)
        delete_button_box2.clicked.connect(self.delete_from_paper)
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
        self.input_research_id_3 = QLineEdit(self)
        self.input_name_3 = QLineEdit(self)
        
        # 将标签和输入框添加到布局中
        box3_layout.addWidget(label3)
        box3_layout.addSpacing(20)
        box3_layout.addWidget(label_research_id_3)
        box3_layout.addStretch(1)
        box3_layout.addWidget(self.input_research_id_3)
        box3_layout.addStretch(1)
        box3_layout.addWidget(label_name_3)
        box3_layout.addStretch(1)
        box3_layout.addWidget(self.input_name_3)
        box3_layout.addStretch(20)
        
        box3.setLayout(box3_layout)

        # 将三个小框添加到水平布局中
        boxes_layout.addWidget(box1)
        boxes_layout.addWidget(box2)
        boxes_layout.addWidget(box3)

        # 按钮
        add_button_box3 = QPushButton('添加', self)
        add_button_box3.clicked.connect(self.add_to_research)
        delete_button_box3 = QPushButton('删除', self)
        delete_button_box3.clicked.connect(self.delete_from_research)
        buttons_layout_box3 = QHBoxLayout()
        buttons_layout_box3.addWidget(add_button_box3)
        buttons_layout_box3.addWidget(delete_button_box3)

        # 将按钮添加到布局
        box3_layout.addLayout(buttons_layout_box3)

        self.setLayout(boxes_layout)

        # 设置标签大小
        font = label1.font()
        font.setBold(True)
        label1.setFont(font)
        label1.setStyleSheet("font-size: 14px;") 

        font = label2.font()
        font.setBold(True)
        label2.setFont(font)
        label2.setStyleSheet("font-size: 14px;") 

        font = label3.font()
        font.setBold(True)
        label3.setFont(font)
        label3.setStyleSheet("font-size: 14px;") 

    # 对teacher的操作
    def add_to_teacher(self): 
        teacher_id = self.input_teacher_id.text().strip() if self.input_teacher_id.text().strip() else None
        rank = self.input_rank.text().strip() if self.input_rank.text().strip() else None
        name = self.input_name.text().strip() if self.input_name.text().strip() else None
        research_id = self.input_research_id.text().strip() if self.input_research_id.text().strip() else None
        laboratory_id = self.input_laboratory_id.text().strip() if self.input_laboratory_id.text().strip() else None
        faculty_id = self.input_faculty_id.text().strip() if self.input_faculty_id.text().strip() else None


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
                # 执行插入操作
                sql_query = 'INSERT INTO teacher (teacher_id, rank, name, research_id, laboratory_id, faculty_id) VALUES (%s, %s, %s, %s, %s, %s)'
                cursor.execute(sql_query, (teacher_id, rank, name, research_id, laboratory_id, faculty_id))

            # 提交事务
            connection.commit()

            # 提示用户插入成功
            QMessageBox.information(self, '成功', '数据插入成功！')

        except Exception as e:
            if e.args[0] == 1062:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入重复值错误：可能是主键冲突')
            elif e.args[0] == 1048:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入空值错误')
            elif e.args[0] == 1452:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '外键约束错误')
            else: 
                connection.rollback()
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()
    def delete_from_teacher(self):
        teacher_id = self.input_teacher_id.text().strip() if self.input_teacher_id.text().strip() else None

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
                # 执行删除操作
                sql_query = 'DELETE FROM teacher WHERE teacher_id = %s'
                affected_rows = cursor.execute(sql_query, (teacher_id))

            # 提交事务
            connection.commit()

            if affected_rows > 0:
                # 提示用户删除成功
                QMessageBox.information(self, '成功', '数据删除成功！')
            else:
                # 提示用户没有匹配的主键记录
                QMessageBox.warning(self, '警告', '没有匹配的主键记录。')

        except Exception as e:
            if e.args[0] == 1451:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '外键约束错误')
            else:
                # 发生错误时回滚
                connection.rollback()

                # 提示用户发生错误
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()

    # 对paper的操作
    def add_to_paper(self): 
        doi = self.input_doi.text().strip() if self.input_doi.text().strip() else None
        title = self.input_title.text().strip() if self.input_title.text().strip() else None
        author = self.input_author.text().strip() if self.input_author.text().strip() else None
        year = self.input_year.text().strip() if self.input_year.text().strip() else None

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
                # 执行插入操作
                sql_query = 'INSERT INTO paper (doi, title, author_id, year) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql_query, (doi, title, author, year))

            # 提交事务
            connection.commit()

            # 提示用户插入成功
            QMessageBox.information(self, '成功', '数据插入成功！')

        except Exception as e:
            if e.args[0] == 1062:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入重复值错误：可能是主键冲突')
            elif e.args[0] == 1048:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入空值错误')
            elif e.args[0] == 1452:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '外键约束错误')
            else: 
                connection.rollback()
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()
    def delete_from_paper(self):
        doi = self.input_doi.text().strip() if self.input_doi.text().strip() else None

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
                # 执行删除操作
                sql_query = 'DELETE FROM paper WHERE doi = %s'
                affected_rows = cursor.execute(sql_query, (doi))

            # 提交事务
            connection.commit()

            if affected_rows > 0:
                # 提示用户删除成功
                QMessageBox.information(self, '成功', '数据删除成功！')
            else:
                # 提示用户没有匹配的主键记录
                QMessageBox.warning(self, '警告', '没有匹配的主键记录。')

        except Exception as e:
            if e.args[0] == 1451:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '外键约束错误')
            else:
                # 发生错误时回滚
                connection.rollback()

                # 提示用户发生错误
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()
    
    # 对research的操作
    def add_to_research(self):
        research_id = self.input_research_id_3.text()
        name = self.input_name_3.text()
        
        research_id = research_id.strip() if research_id.strip() else None # 空字符设置为0
        name = name.strip() if name.strip() else None

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
                # 执行插入操作
                sql_query = 'INSERT INTO research (research_id, name) VALUES (%s, %s)'
                cursor.execute(sql_query, (research_id, name))

            # 提交事务
            connection.commit()

            # 提示用户插入成功
            QMessageBox.information(self, '成功', '数据插入成功！')

        except Exception as e:
            if e.args[0] == 1062:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入重复值错误：可能是主键冲突')
            elif e.args[0] == 1048:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '插入空值错误')
            else: 
                connection.rollback()
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()
    def delete_from_research(self):
        # 获取要删除的 research_id
        research_id_to_delete = self.input_research_id_3.text()
        research_id_to_delete = research_id_to_delete.strip() if research_id_to_delete.strip() else None
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
                # 执行删除操作
                sql_query = 'DELETE FROM research WHERE research_id = %s'
                affected_rows = cursor.execute(sql_query, (research_id_to_delete))

            # 提交事务
            connection.commit()

            if affected_rows > 0:
                # 提示用户删除成功
                QMessageBox.information(self, '成功', '数据删除成功！')
            else:
                # 提示用户没有匹配的主键记录
                QMessageBox.warning(self, '警告', '没有匹配的主键记录。')

        except Exception as e:
            if e.args[0] == 1451:
                # 发生错误时回滚
                connection.rollback()
                # 提示用户发生错误
                QMessageBox.warning(self, '错误', '外键约束错误')
            else:
                # 发生错误时回滚
                connection.rollback()

                # 提示用户发生错误
                QMessageBox.warning(self, '错误', f'发生错误：{str(e)}')

        finally:
            # 完成后关闭数据库连接
            connection.close()
