import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QLabel, 
                             QHeaderView, QPushButton, QFrame)
from PyQt6.QtCore import Qt

def list_folders_and_files(root_dir):
    folder_contents = {}
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            folder_contents[folder_name] = files
    return folder_contents

def create_table_data(folder_contents):
    columns = list(folder_contents.keys())
    rows = []
    max_files = max(len(files) for files in folder_contents.values())
    for i in range(max_files):
        row = [folder_contents[folder][i] if i < len(folder_contents[folder]) else "" for folder in columns]
        rows.append(row)
    table_data = [columns] + rows
    return table_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Contents Grid")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: white;")

        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # File entry and select button
        file_frame = QFrame()
        file_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        file_layout = QHBoxLayout(file_frame)

        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Selected Directory: (Hint: Select a directory)")
        self.file_entry.setReadOnly(True)
        file_layout.addWidget(self.file_entry)

        self.select_button = QPushButton('Select Workspace')
        self.select_button.clicked.connect(self.select_workspace)
        self.select_button.setStyleSheet("background-color: #dcdcdc;")
        file_layout.addWidget(self.select_button)

        main_layout.addWidget(file_frame)

        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget { background-color: #E0FFFF; }
            QTableWidget::item:selected { background-color: #FFA07A; color: black; }
            QHeaderView::section { background-color: #FF4500; color: white; font-weight: bold; }
        """)
        main_layout.addWidget(self.table_widget)

        self.setCentralWidget(main_widget)

    def load_directory(self, dir_path):
        if dir_path:
            folder_contents = list_folders_and_files(dir_path)
            table_data = create_table_data(folder_contents)
            self.display_table(table_data)
            self.file_entry.setText(dir_path)
        else:
            self.file_entry.setText("Selected Directory: (Hint: Select a directory)")

    def display_table(self, data):
        if not data:
            return

        self.table_widget.clear()
        columns = data[0]
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(columns)
        self.table_widget.setRowCount(len(data) - 1)

        for row_idx, row_data in enumerate(data[1:]):
            for col_idx, cell_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(cell_data))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def select_workspace(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.load_directory(dir_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
