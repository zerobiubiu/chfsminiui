import sqlite3

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTableWidget, QHeaderView, \
    QTableWidgetItem, QMessageBox


class openDirWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect('conf.db')
        cur = self.conn.cursor()
        sql_read = 'select * from dir'
        cur.execute(sql_read)
        res = cur.fetchall()
        cur.close()

        self.layout = None
        self.resize(500, 300)
        self.setWindowTitle("addDir")

        self.add = QPushButton('+')
        self.delete = QPushButton('-')

        self.table = QTableWidget(0, 1)
        self.table.setHorizontalHeaderLabels(["Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for re in res:
            item_Dir = QTableWidgetItem(re[0])
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount() - 1, 0, item_Dir)

        self.initTableNumber = self.table.rowCount()

    def showWindow(self):
        self.initUI()
        self.show()

    def initUI(self):
        self.add.clicked.connect(self.FindeDir)
        self.delete.clicked.connect(self.DeleteDir)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.add)
        self.layout.addWidget(self.delete)
        self.layout.addWidget(self.table)

    def FindeDir(self):
        Dir = QtWidgets.QFileDialog.getExistingDirectory()

        if not self.table.findItems(Dir, Qt.MatchFlag.MatchExactly):
            item_Dir = QTableWidgetItem(Dir)
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount() - 1, 0, item_Dir)

    def DeleteDir(self):
        if self.table.currentRow() == -1:
            QMessageBox.warning(self, "警告", "未选择")
        else:
            self.table.removeRow(self.table.currentRow())

    def closeEvent(self, event):
        if self.initTableNumber != 0:
            sql_deleteTable = 'delete from dir where dir="dir"'
            self.conn.cursor().execute(sql_deleteTable)
            self.conn.commit()

        for i in range(self.table.rowCount()):
            sql_temp = f"INSERT into dir(dir) VALUES('{self.table.item(i, 0).text()}')"
            self.conn.cursor().execute(sql_temp)

        self.conn.commit()
        self.conn.close()
