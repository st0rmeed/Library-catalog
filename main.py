import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QLineEdit, \
    QComboBox, QTableWidgetItem, QSizePolicy, QDialog, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 500, 500)
        uic.loadUi('main1.ui', self)

        self.combo.addItems(['Автор', 'Название'])

        self.button.clicked.connect(self.search)

        self.table.setColumnCount(1)
        self.table.horizontalHeader().setHidden(True)
        self.table.verticalHeader().setHidden(True)
        self.table.setRowCount(0)

        self.book_ids = []

    def search(self):
        text = self.combo.currentText()
        search_text = f'%{self.edit.text()}%'

        con = sqlite3.connect("books.sqlite")
        cur = con.cursor()

        if text == 'Автор':
            self.result = cur.execute('''
            SELECT 
                id, title
            FROM 
                books
            WHERE 
                author LIKE ?''', (search_text,)).fetchall()
        else:
            self.result = cur.execute('''
            SELECT 
                id, title
            FROM 
                books
            WHERE 
                title LIKE ?''', (search_text,)).fetchall()

        con.close()

        self.table.setRowCount(0)
        self.table.setRowCount(len(self.result))

        self.book_ids = []

        for i in range(len(self.result)):
            book_id, title = self.result[i]
            button = QPushButton(title)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.table.setRowHeight(i, 30)

            self.book_ids.append(book_id)

            button.clicked.connect(lambda _, bid=book_id: self.show_image(bid))

            self.table.setCellWidget(i, 0, button)

    def show_image(self, book_id):
        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()

        image_data = cur.execute('''
        SELECT 
            image 
        FROM 
            books 
        WHERE id = ?''', (book_id,)).fetchone()

        if image_data and image_data[0]:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data[0])

            image_dialog = QDialog(self)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            layout = QVBoxLayout()
            layout.addWidget(image_label)
            image_dialog.setLayout(layout)
            image_dialog.exec()

        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
