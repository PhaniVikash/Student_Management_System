from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QToolBar,QMessageBox,
                             QGridLayout, QLineEdit, QPushButton, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QStatusBar)
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Student Management System ")
        self.setWindowIcon(QIcon("icons/database.png"))
        self.setMinimumSize(500,500)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"),"Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)


        about_action  = QAction("About",self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

        # Create Toolbar & add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create Status bar and add status bar element
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)


    def cell_clicked(self):

        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)


        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)



    def load_data(self):

        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                print(row_data)
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        #Set layout
        self.setWindowTitle("Insert New Student Details")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        #Add student name
        '''student_name_label = QLabel("Name of student")
        layout.addWidget(student_name_label)'''

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name of the Student :")
        layout.addWidget(self.student_name)

        # Add courses using Combobox
        self.course_name = QComboBox()
        courses = ["Biology",'Maths','Physics','Chemistry','Telugu']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile Number Widget
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Enter Mobile Number :")
        layout.addWidget(self.mobile_number)

        # Add Submit Button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):

        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name , course, mobile) VALUES (?,?,?)",
                       (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        #Set layout
        self.setWindowTitle("Search for student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name of the Student :")
        layout.addWidget(self.student_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = connection.execute("SELECT * FROM students WHERE name = ?",(name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set layout
        self.setWindowTitle("Update New Student Details")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # Extract name to be edited from table
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index,1).text()

        # Get student_id
        self.student_id = main_window.table.item(index,0).text()
        # Add student name
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name of the Student :")
        layout.addWidget(self.student_name)

        # Add courses using Combobox
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", 'Maths', 'Physics', 'Chemistry', 'Telugu','Astronomy']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile Number Widget
        mobile = main_window.table.item(index, 3).text()
        self.mobile_number = QLineEdit(mobile)
        self.mobile_number.setPlaceholderText("Enter Mobile Number :")
        layout.addWidget(self.mobile_number)

        # Add Submit Button
        button = QPushButton("UPDATE")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ? , course = ? ,mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile_number.text(),self.student_id))
        connection.commit()
        cursor.close()
        connection.close()


        #Refresh table
        main_window.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was Successfully Updated")
        confirmation_widget.exec()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set layout
        self.setWindowTitle("Update New Student Details")


        layout = QGridLayout()

        conform = QLabel("Are sure , you want to delete ?")
        yes = QPushButton("Yes")
        no = QPushButton("NO")

        layout.addWidget(conform,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):

        # Get selected index & student_id
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?",(student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was Successfully deleted")
        confirmation_widget.exec()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
