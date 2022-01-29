from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MySQLdb
import datetime
import sys

# to connect our UI file with our python code
from PyQt5.uic import loadUiType
from PyQt5.uic.Compiler.indenter import createCodeIndenter
ui, _ = loadUiType('library.ui')
loginui, _ = loadUiType('login.ui')


class login(QWidget, loginui):
    def __init__(self):  # constructor
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handle_login)
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def handle_login(self):
        user_name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if user_name == 'admin' and password == '123':
            self.window2 = MainApp()
            self.close()
            self.window2.show()
        else:
            self.label_3.setText("*Incorrect username or password!")


# for our main mindow
class MainApp(QMainWindow, ui):
    def __init__(self):  # constructor
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Library Management System')
        self.setWindowIcon(QIcon('libraryicon.png'))
        self.handle_UI_changes()
        self.handle_buttons()
        self.show_category()
        self.show_author()
        self.show_publisher()
        self.dark_orange()
        self.show_all_users()
        self.show_all_books()
        self.show_all_operations()

    def handle_UI_changes(self):
        self.hide_themes()
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        # connecting buttions
        self.pushButton_4.clicked.connect(self.show_themes)
        self.pushButton_24.clicked.connect(self.hide_themes)
        self.pushButton.clicked.connect(self.open_dailyoperations)
        self.pushButton_6.clicked.connect(self.open_books)
        self.pushButton_2.clicked.connect(self.open_users)
        self.pushButton_3.clicked.connect(self.open_settings)
        self.pushButton_7.clicked.connect(self.add_book)
        self.pushButton_16.clicked.connect(self.search_category)
        self.pushButton_18.clicked.connect(self.search_author)
        self.pushButton_19.clicked.connect(self.search_publisher)
        self.pushButton_11.clicked.connect(self.search_book)
        self.pushButton_10.clicked.connect(self.edit_book)
        self.pushButton_12.clicked.connect(self.delete_book)
        self.pushButton_14.clicked.connect(self.add_user)
        self.pushButton_17.clicked.connect(self.login)
        self.pushButton_13.clicked.connect(self.edit_user)
        self.pushButton_20.clicked.connect(self.dark_orange)
        self.pushButton_21.clicked.connect(self.dark_blue)
        self.pushButton_22.clicked.connect(self.qdark)
        self.pushButton_23.clicked.connect(self.dark_grey)
        self.pushButton_8.clicked.connect(self.validate_user)
        self.pushButton_15.clicked.connect(self.day_operations)
        self.pushButton_9.clicked.connect(self.type_operation)

    # methods to handle the themes popup

    def show_themes(self):
        self.groupBox_3.show()

    def hide_themes(self):
        self.groupBox_3.hide()

##########################---Opening Tabs---########################################
    def open_dailyoperations(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings(self):
        self.tabWidget.setCurrentIndex(3)

###############################---BOOKS---##########################################

    def add_book(self):  # connecting databse
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        book_id = self.lineEdit_5.text()
        book_name = self.lineEdit_2.text()
        numofbooks = self.lineEdit_3.text()
        book_description = self.textEdit.toPlainText()
        category_name = self.lineEdit_12.text()
        author_name = self.lineEdit_13.text()
        publisher_name = self.lineEdit_14.text()
        book_price = self.lineEdit_4.text()

        # Inserting values in the books table
        self.cur.execute('''
        INSERT INTO books(book_id, book_name, book_description, book_price, numofbooks)
        VALUES (%s,%s,%s,%s,%s)''',
                         (book_id, book_name, book_description, book_price, numofbooks))

        self.cur.execute('''
        INSERT INTO category(category_name, book_id)
        VALUES (%s, %s)''',
                         (category_name, book_id))

        self.cur.execute('''
        INSERT INTO authors(author_name, book_id)
        VALUES (%s, %s)''',
                         (author_name, book_id))

        self.cur.execute('''
        INSERT INTO publishers(publisher_name, book_id)
        VALUES (%s, %s)''',
                         (publisher_name, book_id))

        self.db.commit()
        self.statusBar().showMessage('New Book Added!')

        # Emptying fields after a new book is added
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.show_all_books()

    def search_book(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        # book_name = self.lineEdit_7.text()
        book_id = self.lineEdit_11.text()

        sql = '''SELECT * FROM books WHERE book_id=%s'''
        self.cur.execute(sql, [(book_id)])

        data = self.cur.fetchone()

        # printing search results in respective fields
        self.lineEdit_10.setText(str(data[0]))
        self.lineEdit_8.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_9.setText(str(data[3]))
        self.lineEdit_6.setText(str(data[4]))

        sql2 = '''SELECT * FROM category WHERE book_id= %s'''
        self.cur.execute(sql2, [(book_id)])
        data2 = self.cur.fetchone()
        self.lineEdit_15.setText(data2[1])

        sql3 = '''SELECT * FROM authors WHERE book_id= %s'''
        self.cur.execute(sql3, [(book_id)])
        data3 = self.cur.fetchone()
        self.lineEdit_16.setText(data3[1])

        sql4 = '''SELECT * FROM publishers WHERE book_id= %s'''
        self.cur.execute(sql4, [(book_id)])
        data4 = self.cur.fetchone()
        self.lineEdit_25.setText(data4[1])

    def edit_book(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        book_id = self.lineEdit_10.text()
        book_name = self.lineEdit_8.text()
        numofbooks = self.lineEdit_6.text()
        book_description = self.textEdit_2.toPlainText()
        book_category = self.lineEdit_15.text()
        book_author = self.lineEdit_16.text()
        book_publisher = self.lineEdit_25.text()
        book_price = self.lineEdit_9.text()
        searched_bookid = self.lineEdit_11.text()

        self.cur.execute(''' 
        UPDATE books SET book_id=%s,book_name=%s,book_description=%s,book_price=%s,numofbooks=%s WHERE book_id = %s
        ''', (book_id, book_name, book_description, book_price, numofbooks, searched_bookid))

        self.cur.execute('''
        UPDATE category SET book_id=%s,category_name=%s WHERE book_id=%s''',
                         (book_id, book_category, searched_bookid))

        self.cur.execute('''
        UPDATE authors SET book_id=%s,author_name=%s WHERE book_id=%s''',
                         (book_id, book_author, searched_bookid))

        self.cur.execute('''
        UPDATE publishers SET book_id=%s,publisher_name=%s WHERE book_id=%s''',
                         (book_id, book_publisher, searched_bookid))

        self.db.commit()
        self.statusBar().showMessage('Book Details Updated!')
        self.show_all_books()

    def delete_book(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()     #

        searched_bookid = self.lineEdit_11.text()

        sql2 = '''DELETE FROM category WHERE book_id = %s'''
        self.cur.execute(sql2, ([searched_bookid]))

        sql3 = '''DELETE FROM authors WHERE book_id = %s'''
        self.cur.execute(sql3, ([searched_bookid]))

        sql4 = '''DELETE FROM publishers WHERE book_id = %s'''
        self.cur.execute(sql4, ([searched_bookid]))

        sql = '''DELETE FROM books WHERE book_id = %s'''
        self.cur.execute(sql, ([searched_bookid]))

        self.db.commit()
        self.statusBar().showMessage('Book Deleted!')

        self.lineEdit_10.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_6.setText('')
        self.textEdit_2.setPlainText('')
        self.lineEdit_15.setText('')
        self.lineEdit_16.setText('')
        self.lineEdit_25.setText('')
        self.lineEdit_9.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_7.setText('')

        self.show_all_books()

    def show_all_books(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT books.book_id, book_name, book_description, category_name, author_name, publisher_name 
                            FROM books 
                            INNER JOIN category ON books.book_id = category.book_id 
                            INNER JOIN authors ON books.book_id = authors.book_id 
                            INNER JOIN publishers ON books.book_id = publishers.book_id''')
        data = self.cur.fetchall()
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_6.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1

                rownum = self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(rownum)

        self.db.close()


#################################---USERS---#########################################


    def add_user(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()

        user_id = self.lineEdit_26.text()
        user_name = self.lineEdit_21.text()
        user_email = self.lineEdit_22.text()
        password = self.lineEdit_23.text()
        repassword = self.lineEdit_24.text()
        user_cnic = self.lineEdit_32.text()

        if password == repassword:
            self.cur.execute(''' 
            INSERT INTO users(user_id,user_name,user_email, user_cnic, user_password)
            VALUES(%s, %s, %s, %s, %s) ''', (user_id, user_name, user_email, user_cnic, password))

            self.db.commit()
            self.statusBar().showMessage('New User Added!')

            self.lineEdit_21.setText('')
            self.lineEdit_22.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_24.setText('')
            self.label_43.setText('')
            self.lineEdit_32.setText('')
            self.lineEdit_26.setText('')
        else:
            self.label_43.setText('*passwords donot match!')
            self.lineEdit_24.setText('')

    def login(self):

        user_name = self.lineEdit_28.text()
        password = self.lineEdit_31.text()

        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()

        sql = '''SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if user_name == row[1] and password == row[4]:
                self.statusBar().showMessage('Valid User!')
                self.groupBox_5.setEnabled(True)

                self.lineEdit_37.setText(str(row[0]))
                self.lineEdit_20.setText(row[1])
                self.lineEdit_19.setText(row[2])
                self.lineEdit_33.setText(str(row[3]))
                self.lineEdit_18.setText(str(row[4]))
            else:
                self.statusBar().showMessage('Invalid User!')

    def edit_user(self):
        previous_userid = self.lineEdit_28.text()
        user_id = self.lineEdit_37.text()
        user_name = self.lineEdit_20.text()
        user_email = self.lineEdit_19.text()
        user_cnic = self.lineEdit_33.text()
        password = self.lineEdit_18.text()
        repassword = self.lineEdit_17.text()

        if password == repassword:
            self.db = MySQLdb.connect(
                host='localhost', user='root', password='123', db='lib')
            self.cur = self.db.cursor()

            self.cur.execute('''UPDATE users SET user_id=%s, user_name=%s, user_email=%s,user_cnic=%s, user_password=%s WHERE user_name=%s''',
                             (user_id, user_name, user_email, user_cnic, password, previous_userid))

            self.db.commit()
            self.statusBar().showMessage('User Information Updated!')
            self.label_30.setText('')
            self.show_all_users()

        else:
            self.label_30.setText('passwords donot match!')
            self.lineEdit_16.setText('')

    def show_all_users(self):

        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()

        self.cur.execute(
            '''SELECT user_id, user_name, user_email, user_cnic FROM users ''')
        data = self.cur.fetchall()

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1

                rownum = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(rownum)

        self.db.close()


#################################---SETTINGS TAB---#########################################


    def search_category(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        category_name = self.lineEdit_27.text()

        sql = '''SELECT * FROM category'''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if category_name == row[1]:
                self.statusBar().showMessage('Valid Category!')
                self.show_category()
            else:
                self.statusBar().showMessage('Category not Found!')
                self.lineEdit_27.setText('')

        self.db.commit()  # commiting change in the DB
        self.show_category()

    def show_category(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        category_name = self.lineEdit_27.text()

        # getting category data from DB and storing in 'data'
        sql = '''SELECT category.book_id, book_name FROM category 
                 INNER JOIN books ON category.book_id = books.book_id
                 WHERE category_name =%s'''
        self.cur.execute(sql, [(category_name)])
        data = self.cur.fetchall()

        # prints data in the table widget
        if data:
            # clears previous data in lineEdits
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)     # inserts an empty row
            # enumerate counts the number of iterations
            for row, form in enumerate(data):
                # loops to print data in TabWidget
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def search_author(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        author_name = self.lineEdit_29.text()
        sql = '''SELECT * FROM authors'''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if author_name == row[1]:
                self.statusBar().showMessage('Valid Author!')
                self.show_author()
                return
            else:
                self.statusBar().showMessage('Author not Found!')
                self.lineEdit_29.setText('')

    def show_author(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        author_name = self.lineEdit_29.text()

        sql = '''SELECT authors.book_id, book_name FROM authors 
                 INNER JOIN books ON authors.book_id = books.book_id
                 WHERE author_name =%s'''
        self.cur.execute(sql, [(author_name)])
        data = self.cur.fetchall()

        # prints data in the table widget
        if data:
            # clears previous data in lineEdits
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)     # inserts an empty row
            # enumerate counts the number of iterations
            for row, form in enumerate(data):
                # loops to print data in TabWidget
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    def search_publisher(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        publisher_name = self.lineEdit_30.text()
        sql = '''SELECT * FROM publishers'''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if publisher_name == row[1]:
                self.statusBar().showMessage('Valid Publisher!')
                self.show_publisher()
            else:
                self.statusBar().showMessage('Publisher not Found!')
                self.lineEdit_30.setText('')

    def show_publisher(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        publisher_name = self.lineEdit_30.text()

        sql = '''SELECT publishers.book_id, book_name FROM publishers 
                 INNER JOIN books ON publishers.book_id = books.book_id
                 WHERE publisher_name =%s'''
        self.cur.execute(sql, [(publisher_name)])
        data = self.cur.fetchall()

        # prints data in the table widget
        if data:
            # clears previous data in lineEdits
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)     # inserts an empty row
            # enumerate counts the number of iterations
            for row, form in enumerate(data):
                # loops to print data in TabWidget
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)


#################################---THEMES---##############################

    def dark_blue(self):
        style = open('themes/darkblue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_grey(self):
        style = open('themes/darkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qdark(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


##############################---DAY OPERATIONS---############################


    def validate_user(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()  # adding cursor

        user_id = self.lineEdit_34.text()
        user_name = self.lineEdit_35.text()

        sql = '''SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if user_id == str(row[0]) and user_name == row[1]:
                self.statusBar().showMessage('Valid User!')
                self.groupBox_4.setEnabled(True)

    def type_operation(self):
        op = self.comboBox.currentIndex()
        if op == 1:
            self.comboBox_2.clear()
            self.label_2.setText('')
            self.groupBox_6.setEnabled(True)
        else:
            self.groupBox_6.setEnabled(True)
            self.comboBox_2.setEnabled(True)

    def day_operations(self):
        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()

        book_name = self.lineEdit.text()
        book_id = self.lineEdit_36.text()
        days = self.comboBox_2.currentIndex() + 1
        type = self.comboBox.currentText()
        op_date = datetime.date.today()
        user_id = self.lineEdit_34.text()
        user_name = self.lineEdit_35.text()
        from_date = datetime.date.today()
        to_date = from_date + datetime.timedelta(days=int(days))
        op = self.comboBox.currentIndex()

        if op == 1:
            self.cur.execute('''INSERT INTO dayoperations(op_date, book_id, user_id, type, days, from_date, to_date)
                            VALUES (%s, %s, %s, %s,DEFAULT,DEFAULT,%s) ''', (op_date, book_id, user_id, type, to_date))
            self.db.commit()
            self.statusBar().showMessage('New Operation Added!')
            self.show_all_operations()
            self.lineEdit_36.setText('')
            self.lineEdit.setText('')
            return

        self.cur.execute('''INSERT INTO dayoperations(op_date, book_id, user_id, type, days, from_date, to_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s) ''', (op_date, book_id, user_id, type, days, from_date, to_date))
        self.db.commit()
        self.statusBar().showMessage('New Operation Added!')
        self.lineEdit_36.setText('')
        self.lineEdit.setText('')
        self.show_all_operations()

    def show_all_operations(self):

        self.db = MySQLdb.connect(
            host='localhost', user='root', password='123', db='lib')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT op_date, users.user_name, books.book_name, type, from_date, to_date FROM dayoperations
                            INNER JOIN books ON books.book_id = dayoperations.book_id
                            INNER JOIN users ON users.user_id = dayoperations.user_id;''')

        data = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)


###########################---MAIN---#############################################

def main():
    app = QApplication(sys.argv)
    window = login()
    window.setWindowTitle('Login')
    window.setWindowIcon(QIcon('loginicon.png'))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
