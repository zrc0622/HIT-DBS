from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QTreeWidgetItem, QStyleFactory
from gui import Ui_MainWindow
import sys

query0 = '''SELECT [ ENAME = 'Mary' & DNAME = 'Research' ] ( EMPLOYEE JOIN DEPARTMENT )'''
query1 = '''PROJECTION [ BDATE ] ( SELECT [ ENAME = 'John' & DNAME = 'Research' ] ( EMPLOYEE JOIN DEPARTMENT ) )'''
query2 = '''SELECT [ ESSN = '01' ] ( PROJECTION [ ESSN, PNAME ] ( WORKS_ON JOIN PROJECT ) )'''

queries = [query0, query1, query2]


class TreeNode:
    def __init__(self, op='', info=''):
        self.child = []  # 儿子节点
        self.op = op
        self.info = info

    def __str__(self):
        return (self.op if self.op else '') + (' ' + self.info if self.info else '')


class MainWindow(QMainWindow):
    def __init__(self, ui_main_win: Ui_MainWindow):
        super().__init__()
        self.ui = ui_main_win
        ui_main_win.setupUi(self)
        self.set_query()

    # 设置表格显示
    def set_query(self):
        self.ui.query_table.setRowCount(len(queries))
        self.ui.query_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.query_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for idx, query in enumerate(queries):
            self.ui.query_table.setItem(idx, 0, QTableWidgetItem('  query%d  ' % idx))
            self.ui.query_table.setItem(idx, 1, QTableWidgetItem(query))
        self.ui.query_box.addItems(['query%d' % idx for idx in range(len(queries))])

    def query(self):
        root = get_tree(queries[self.ui.query_box.currentIndex()])
        if self.ui.optimize_on.isChecked():
            root = optimize(root)

        tree_stack, item_stack = [root], [QTreeWidgetItem(self.ui.parse_tree)]

        while tree_stack:
            tree_node, item_node = tree_stack.pop(0), item_stack.pop(0)
            item_node.setText(0, str(tree_node))
            tree_stack = tree_node.child + tree_stack
            item_stack = [QTreeWidgetItem(item_node) for child in tree_node.child] + item_stack
        self.ui.parse_tree.expandAll()
        self.ui.parse_tree.setStyle(QStyleFactory.create('windows'))
        self.ui.parse_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)


def get_tree(query: str):
    tokens, idx, node = query.split(), 0, TreeNode()
    while idx < len(tokens):
        token = tokens[idx]
        if token == 'SELECT' or token == 'PROJECTION':
            end = tokens.index(']', idx)
            node.op, node.info = token, ' '.join(tokens[idx + 2:end])
            idx = end + 1
        elif token == 'JOIN':
            node.op = token
            node.child.append(TreeNode(info=tokens[idx - 1]))  # 连接操作的第一个关系
            node.child.append(TreeNode(info=tokens[idx + 1]))  # 连接操作的第二个关系
            idx += 1
        elif token == '(':  # 括号内为查询子句，字句所在的子树应该更靠近叶节点
            count, idy = 1, idx + 1
            while idy < len(tokens) and count > 0:
                if tokens[idy] == '(':
                    count += 1
                elif tokens[idy] == ')':
                    count -= 1
                idy += 1
            node.child.append(get_tree(' '.join(tokens[idx + 1:idy - 1])))
            idx = idy
        else:
            idx += 1
    return node


def output_tree(node: TreeNode, sep=''):
    print(sep + str(node))
    if len(node.child) >= 1:
        output_tree(node.child[0], sep + '\t')
    if len(node.child) >= 2:
        output_tree(node.child[1], sep + '\t')


def optimize(node: TreeNode, info_lst=None) -> TreeNode:
    if node.op == 'SELECT':
        node = optimize(node.child[0], node.info.split('&'))
    elif node.op == 'PROJECTION':
        node.child[0] = optimize(node.child[0], info_lst)
    elif node.op == 'JOIN':
        node0 = TreeNode(op='SELECT', info=info_lst[0])
        node0.child.append(node.child[0])
        node.child[0] = node0
        if len(info_lst) > 1:
            node1 = TreeNode(op='SELECT', info=info_lst[1])
            node1.child.append(node.child[1])
            node.child[1] = node1
    return node


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow(Ui_MainWindow())
    main_win.show()
    sys.exit(app.exec_())

'''
用户界面（UI）：

代码使用 PyQt5 创建了一个图形用户界面（UI），用于显示 SQL 查询及其相应的解析树。
用户界面类（Ui_MainWindow）：

该类是由 Qt Designer 或类似工具生成的，定义了主窗口的结构。
主应用程序类（MainWindow）：

该类继承自 QMainWindow，负责主要的应用程序逻辑。
__init__ 方法初始化主窗口，使用提供的 Ui_MainWindow 实例设置用户界面，并调用 set_query 方法填充查询表。
set_query 方法用示例查询填充查询表。
query 方法与“生成查询树”按钮连接，当按钮被点击时调用。它从组合框中获取所选查询，使用 get_tree 函数将其解析为树结构，可选地使用 optimize 函数优化树，然后在解析树窗口中显示该树。
查询树节点类（TreeNode）：

该类表示解析树中的节点。每个节点都有一个操作（op）、信息（info）和一个子节点列表。
查询解析函数（get_tree 和 optimize）：

get_tree 函数接受一个 SQL 查询作为输入，并递归构建了一个由 TreeNode 对象表示的解析树。它处理了查询中的 SELECT、PROJECTION、JOIN 和括号。
optimize 函数接受一个解析树节点，并对树进行优化。它专门处理 SELECT、PROJECTION 和 JOIN 操作的优化。
应用程序入口点（`if name == 'main':）：

代码的这部分初始化了 PyQt 应用程序，创建了 MainWindow 类的实例，并显示主窗口。
'''