import sqlite3
import subprocess
import sys

from PySide6.QtWidgets import QApplication, QPushButton, QSpinBox, QWidget

from component.dir import openDirWindow
from component.user import userManagement
from component.judgeOS import judgeOS

class startWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cmd = None

        self.resize(200, 150)
        self.port = QSpinBox(self)
        self.port.resize(65, 20)
        self.port.move(30, 30)
        self.port.setMaximum(65535)
        self.port.setMinimum(0)
        self.port.setValue(self.getPort())

        self.start = QPushButton("启动", self)
        self.start.setCheckable(True)
        self.start.move(110, 25)
        self.start.clicked.connect(self.startCHFS)

        self.openDir = openDirWindow()
        self.openUser = userManagement()

        self.openDirButton = QPushButton("启动目录", self)
        self.openDirButton.clicked.connect(self.openDir.showWindow)
        self.openDirButton.move(50, 60)

        self.openUserButton = QPushButton("用户管理", self)
        self.openUserButton.clicked.connect(self.openUser.showWindow)
        self.openUserButton.move(50, 90)

        self.show()

    def numPers(self, pers):
        numbers = {
            0: "",
            1: "r",
            2: "w",
            3: "rw",
            4: "d",
            5: "rd",
            6: "wd",
            7: "rwd"
        }
        return numbers.get(pers, None)

    def getPort(self):
        conn = sqlite3.connect('conf.db')
        res = conn.cursor().execute('select * from port').fetchall()
        port = res[0][0]
        conn.close()
        return port

    def startCHFS(self):
        port = self.port.value()
        state = self.start.isChecked()
        chfs = judgeOS()
        path = ""
        rule = ""
        conn = sqlite3.connect('conf.db')
        res = conn.cursor().execute('select * from dir').fetchall()
        resu = conn.cursor().execute('select * from user').fetchall()
        conn.close()

        for re in res:
            if enumerate(res) == 1:
                path = f"{re[0]}"
            else:
                path = f"{path}{re[0]}|"

        for re in resu:
            if enumerate(res) == 0:
                rule = "::rwd"
            elif enumerate(res) == 1:
                rule = f"{re[0]}:{re[1]}:{self.numPers(re[2])}"
            else:
                rule = f"{rule}{re[0]}:{re[1]}:{self.numPers(re[2])}|"

        if state:
            self.cmd = subprocess.Popen(["./runapp/"+ str(chfs), "--port=" + str(port), "--path=" + str(path), "--rule=" + str(rule)])
        else:
            self.cmd.terminate()

    def closeEvent(self, event):
        conn = sqlite3.connect('conf.db')
        conn.cursor().execute('delete from port where port="port"')
        conn.commit()
        conn.cursor().execute(f'INSERT INTO port("port")VALUES ({self.port.value()});')
        conn.commit()
        conn.close()
        self.cmd.terminate()


def main():
    app = QApplication()
    start = startWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
