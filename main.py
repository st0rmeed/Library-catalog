import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QLineEdit, \
    QComboBox, QTableWidgetItem, QSizePolicy, QDialog, QLabel, QHBoxLayout, QFormLayout
from PyQt6.QtGui import QPixmap
from PyQt6 import uic


class BookInfoDialog(QDialog):
    def __init__(self, book_id):
        super().__init__()
        layout = QVBoxLayout()

        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        result = cur.execute('''
            SELECT 
                title, author, year, genre, image 
            FROM 
                books 
            WHERE id = ?''', (book_id,)).fetchone()
        con.close()

        if result:
            title, author, year, genre, image_data = result

            if image_data is not None and len(image_data) > 0:
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
            else:
                pixmap = QPixmap('default.jpg')

            image_label = QLabel()
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)

            form_layout = QFormLayout()
            form_layout.addRow('Название:', QLabel(title))
            form_layout.addRow('Автор:', QLabel(author))
            form_layout.addRow('Год издания:', QLabel(str(year)))
            form_layout.addRow('Жанр:', QLabel(genre))
            layout.addLayout(form_layout)

            self.setLayout(layout)
        else:
            self.close()


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
        search_field = self.combo.currentText()
        search_text = f'%{self.edit.text()}%'

        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()

        if search_field == 'Автор':
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
        dialog = BookInfoDialog(book_id)
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
