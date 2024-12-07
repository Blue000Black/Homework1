from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog
import sys
import sqlite3

class Winedit(QDialog):
    def __init__(self):
        super().__init__()
        global win
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('CoffeEdit')
        self.btncommit.clicked.connect(self.commit)
        self.btnadd.clicked.connect(self.addrow)
        self.btndel.clicked.connect(self.delrow)
        self.btnotm.clicked.connect(self.hide)
        self.con = sqlite3.connect('coffee.sqlite')
        self.curs = self.con.cursor()
        self.data = self.curs.execute('SELECT * FROM coffes').fetchall()
        self.table.setRowCount(0)
        for i, row in enumerate(self.data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j > 0:
                    self.table.setItem(i, j - 1, QTableWidgetItem(str(elem)))

    def addrow(self):
        self.table.setRowCount(self.table.rowCount() + 1)

    def delrow(self):
        self.table.setRowCount(self.table.rowCount() - 1)

    def commit(self):
        global win
        for i in range(self.table.rowCount()):
            self.con.cursor().execute(f"""UPDATE coffes 
    SET name = ?, stage = ?, type = ?, taste = ?, price = ?, v = ?
    WHERE id = {i}""",
                tuple([str(self.table.item(i, j).text()) for j in range(6)]))
        self.con.commit()
        win.update()
        self.hide()

    def closeEvent(self, event):
        global win
        self.con.close()
        win.close()


class CoffeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('CoffeInfo')
        self.con = sqlite3.connect('coffee.sqlite')
        self.curs = self.con.cursor()
        self.data = self.curs.execute('SELECT * FROM coffes').fetchall()
        self.table.setRowCount(0)
        for i, row in enumerate(self.data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j > 0:
                    self.table.setItem(i, j - 1, QTableWidgetItem(str(elem)))
        self.btnedit.clicked.connect(self.edit)

    def edit(self):
            global winedit
            winedit.table.setRowCount(0)
            for i, row in enumerate(self.data):
                winedit.table.setRowCount(winedit.table.rowCount() + 1)
                for j, elem in enumerate(row):
                    if j > 0:
                        winedit.table.setItem(i, j - 1, QTableWidgetItem(str(elem)))
            winedit.show()

    def update(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.curs = self.con.cursor()
        self.data = self.curs.execute('SELECT * FROM coffes').fetchall()
        self.table.setRowCount(0)
        for i, row in enumerate(self.data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j > 0:
                    self.table.setItem(i, j - 1, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.con.close()


import traceback
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)
sys.excepthook = excepthook


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CoffeInfo()
    win.show()
    winedit = Winedit()
    sys.exit(app.exec())