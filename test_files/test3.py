import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
def show_message_box():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText("This is a message box")
    msg_box.setInformativeText("This is additional information")
    msg_box.setWindowTitle("Message Box")