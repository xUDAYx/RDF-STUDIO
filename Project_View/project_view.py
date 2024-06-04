import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QTableWidget,
                             QTableWidgetItem, QPushButton, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal

def list_folders_and_files(root_dir):
    folder_contents = {}
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            folder_contents[folder_name] = files
    return folder_contents

def group_files_by_prefix(folder_contents):
    file_groups = {}
    for folder_name, files in folder_contents.items():
        for file_name in files:
            prefix = get_prefix(file_name)
            if prefix not in file_groups:
                file_groups[prefix] = {'RDF_BF': None, 'RDF_BVO': None, 'RDF_JSON': None, 'RDF_JS_OBJ': None, 'RDF_UI': None}
            if 'BF' in file_name:
                file_groups[prefix]['RDF_BF'] = file_name
            elif 'BVO' in file_name:
                file_groups[prefix]['RDF_BVO'] = file_name
            elif 'Data' in file_name:
                file_groups[prefix]['RDF_JSON'] = file_name
            elif 'Action' in file_name:
                file_groups[prefix]['RDF_JS_OBJ'] = file_name
            elif 'UI' in file_name:
                file_groups[prefix]['RDF_UI'] = file_name
    return file_groups

def create_table_data(file_groups):
    columns = ['RDF_UI', 'RDF_JS_OBJ', 'RDF_JSON', 'RDF_BVO', 'RDF_BF']
    rows = []
    for _, file_group in file_groups.items():
        rows.append([file_group['RDF_UI'], file_group['RDF_JS_OBJ'], file_group['RDF_JSON'], file_group['RDF_BVO'], file_group['RDF_BF']])
    table_data = [columns] + rows
    return table_data

def get_prefix(filename):
    return filename.split('BF')[0] if 'BF' in filename else \
           filename.split('BVO')[0] if 'BVO' in filename else \
           filename.split('Data')[0] if 'Data' in filename else \
           filename.split('Action')[0] if 'Action' in filename else \
           filename.split('UI')[0] if 'UI' in filename else filename

class ProjectView(QWidget):
    file_double_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Contents Grid")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)

        # File entry and select/refresh buttons
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

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_directory)
        self.refresh_button.setStyleSheet("background-color: #dcdcdc;")
        file_layout.addWidget(self.refresh_button)

        main_layout.addWidget(file_frame)

        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget { background-color: #E0FFFF; }
            QTableWidget::item:selected { background-color: #FFA07A; color: black; }
            QHeaderView::section { background-color: #FF4500; color: white; font-weight: bold; }
        """)
        self.table_widget.cellDoubleClicked.connect(self.cell_double_clicked)
        main_layout.addWidget(self.table_widget)

        self.load_directory('')
        self.folder_path = ''

    def load_directory(self, dir_path):
        if dir_path:
            folder_contents = list_folders_and_files(dir_path)
            # Set folder_path *before* calling other functions
            self.folder_path = dir_path
            file_groups = group_files_by_prefix(folder_contents)
            table_data = create_table_data(file_groups)
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
                item = QTableWidgetItem(cell_data)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # Make item non-editable
                self.table_widget.setItem(row_idx, col_idx, item)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def select_workspace(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.load_directory(dir_path)

    def refresh_directory(self):
        if self.folder_path:
            self.load_directory(self.folder_path)
        else:
            self.file_entry.setText("Selected Directory: (Hint: Select a directory)")

    def cell_double_clicked(self, row, column):
        folder_name = self.table_widget.horizontalHeaderItem(column).text()
        file_name_item = self.table_widget.item(row, column)
        if file_name_item:
            file_name = file_name_item.text()
            if file_name:
                file_path = os.path.join(self.folder_path, folder_name, file_name)
                self.file_double_clicked.emit(file_path)

# If this script is run directly, create a QApplication and show the ProjectView window
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ProjectView()
    window.show()
    sys.exit(app.exec())