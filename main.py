from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon, QPixmap)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QTextEdit, QStatusBar, QWidget, QFileDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton as DialogButton)
import subprocess

global selected_files
selected_files  = []

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 273)
        MainWindow.setStyleSheet("background-color: rgb(7, 7, 7); color: rgb(145, 145, 145);")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setGeometry(QRect(20, 10, 511, 231))
        self.textEdit.setStyleSheet(
            "background-color: rgb(20, 20, 20);"
            "border: 1px solid rgb(140, 0, 2);"
            "color: rgb(220, 220, 220);"
            "border-radius: 5px;"
        )

        button_style = (
            "QPushButton {"
            "border: 2px solid rgb(140, 0, 2);"
            "background-color: rgb(40, 40, 40);"
            "color: rgb(220, 220, 220);"
            "border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "border: 2px solid rgb(255, 255, 255);"
            "box-shadow: 0px 0px 10px white;"
            "}"
        )

        font = QFont()
        font.setPointSize(18)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QRect(550, 10, 81, 71))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(button_style)
        icon = QIcon(QIcon.fromTheme("document-send"))
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(20, 20))

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setGeometry(QRect(550, 90, 81, 71))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(button_style)
        icon1 = QIcon(QIcon.fromTheme("document-open"))
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QSize(20, 20))

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setGeometry(QRect(550, 170, 81, 71))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(button_style)
        icon2 = QIcon(QIcon.fromTheme("call-start"))
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QSize(20, 20))

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(650, 0, 41, 251))
        self.label.setPixmap(QPixmap("logo.png"))
        self.label.setScaledContents(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.sender = Sender(self.textEdit)
        self.pushButton.clicked.connect(self.sender.send_text)

        self.pushButton_2.clicked.connect(self.select_files)

        self.pushButton_3.clicked.connect(self.open_phone_number_dialog)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "WMS - Lite | #CREW2022", None))
        self.pushButton.setText("")
        self.pushButton_2.setText("")
        self.pushButton_3.setText("")
        self.label.setText("")

    def select_files(self):
        global selected_files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*.*)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.handle_selected_files(selected_files)

    def handle_selected_files(self, files):
        global selected_files
        selected_files = ['']
        self.selected_files = ['']
        self.selected_files = files
        selected_files = self.selected_files

        print("Selected files:", self.selected_files)

    def open_phone_number_dialog(self):
        dialog = PhoneNumberDialog(self)
        dialog.exec()

class Sender:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.phone_numbers = []

    def send_text(self):
        global selected_files
        print(len(selected_files))
        message = self.text_edit.toPlainText()
        print("Message:", message)

        if message and self.phone_numbers:
            for phone_number in self.phone_numbers:
                if len(selected_files) > 0:
                    for file in selected_files:
                        try:
                            subprocess.run(['npx', 'mudslide@latest', 'send-image', '--caption', message, phone_number, file], check=True)
                            print(f"Message and file sent to {phone_number} successfully.")
                        except subprocess.CalledProcessError as e:
                            print(f"Error sending message to {phone_number}: {e}")
                        except Exception as e:
                            print(f"Unexpected error: {e}")
                else:
                    try:
                        subprocess.run(['npx', 'mudslide@latest', 'send', phone_number , message], check=True)
                        print(f"Message sent to {phone_number} successfully.")
                    except subprocess.CalledProcessError as e:
                        print(f"Error sending message to {phone_number}: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
        else:
            print("No message or phone numbers to send.")

    def update_phone_numbers(self, phone_numbers):
        self.phone_numbers = phone_numbers
        print("Phone numbers updated:", self.phone_numbers)

class PhoneNumberDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Enter Phone Numbers")
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout(self)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter phone numbers (separated by commas and with 94)")
        self.layout.addWidget(self.phone_input)

        self.save_button = DialogButton(self)
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save_phone_numbers)
        self.layout.addWidget(self.save_button)

        self.phone_numbers = []

    def save_phone_numbers(self):
        raw_input = self.phone_input.text()
        self.phone_numbers = [num.strip() for num in raw_input.split(',')]
        print("Phone Numbers:", self.phone_numbers)

        self.parent().sender.update_phone_numbers(self.phone_numbers)

        self.accept()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
