from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
import sqlite3


class CoffeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.curs = self.con.cursor()
        self.data = self.curs.execute('SELECT * FROM coffes').fetchall()
        self.table.setRowCount(5)
        for i, row in enumerate(self.data):
            for j, elem in enumerate(row):
                if j > 0:
                    self.table.setItem(i, j - 1, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.con.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CoffeInfo()
    win.show()
    sys.exit(app.exec())