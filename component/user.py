import sqlite3

from PySide6.QtWidgets import QWidget, QTableWidget, QHeaderView, QApplication, QVBoxLayout, QTableWidgetItem, \
    QPushButton, QMessageBox


class userManagement(QWidget):
    def __init__(self):
        super().__init__()

        conn = sqlite3.connect('conf.db')
        cur = conn.cursor()
        sql_read = 'select * from user'
        cur.execute(sql_read)
        res = cur.fetchall()
        cur.close()
        conn.close()

        self.resize(500, 300)
        self.setWindowTitle("userManagement")

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["用户", "密码", "权限"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.add = QPushButton('+')
        self.add.clicked.connect(self.addNewLine)
        self.delete = QPushButton('-')
        self.delete.clicked.connect(self.delLine)

        self.layout = None
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.add)
        self.layout.addWidget(self.delete)
        self.layout.addWidget(self.table)

        for re in res:
            item_user = QTableWidgetItem(re[0])
            item_pass = QTableWidgetItem(re[1])
            item_pers = QTableWidgetItem(str(re[2]))
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount()-1, 0, item_user)
            self.table.setItem(self.table.rowCount()-1, 1, item_pass)
            self.table.setItem(self.table.rowCount()-1, 2, item_pers)

        self.initTableNumber = self.table.rowCount()

    def showWindow(self):
        self.show()

    def addNewLine(self):
        self.table.insertRow(self.table.rowCount())
        item = QTableWidgetItem("0")
        self.table.setItem(self.table.rowCount() - 1, 2, item)

    def delLine(self):
        if self.table.currentRow() == -1:
            QMessageBox.warning(self, "警告", "未选择")
        else:
            self.table.removeRow(self.table.currentRow())

    def closeEvent(self, event):
        conn = sqlite3.connect('conf.db')

        if self.initTableNumber != 0:
            sql_deleteTable = 'delete from user where permissions="permissions"'
            conn.cursor().execute(sql_deleteTable)
            conn.commit()

        for i in range(self.table.rowCount()):
            sql_temp = f'INSERT INTO user("user", "passwd", "permissions") VALUES("{self.table.item(i, 0).text()}", "{self.table.item(i, 1).text()}", "{self.table.item(i, 2).text()}")'
            conn.cursor().execute(sql_temp)
            conn.commit()

        conn.close()