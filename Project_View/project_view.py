import os
import re
import logging
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
                file_groups[prefix] = {'RDF_UI': None, 'RDF_JS_OBJ': None, 'RDF_BF': None, 'RDF_BVO': None, 'RDF_JSON': None}
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
    with open('readme.txt', 'r') as file:
        main_file = file.read().split(':')[1].strip()

    columns = ['RDF_UI', 'RDF_JS_OBJ', 'RDF_BF', 'RDF_BVO', 'RDF_JSON']
    rows = []
    main_file_group = {'RDF_UI': main_file, 'RDF_JS_OBJ': None, 'RDF_BF': None, 'RDF_BVO': None, 'RDF_JSON': None}

    for prefix, file_group in file_groups.items():
        if file_group['RDF_UI'] == main_file:
            main_file_group.update(file_group)
            break

    for _, file_group in file_groups.items():
        rows.append([file_group['RDF_UI'], file_group['RDF_JS_OBJ'], file_group['RDF_BF'], file_group['RDF_BVO'], file_group['RDF_JSON']])

    table_data = [columns, list(main_file_group.values())] + rows
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
        file_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; height: 20px; padding: 2px;")
        file_layout = QHBoxLayout(file_frame)

        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Selected Directory: (Hint: Select a directory)")
        self.file_entry.setReadOnly(True)
        self.file_entry.setStyleSheet("border-radius: 5px;")
        file_layout.addWidget(self.file_entry)

        self.select_button = QPushButton('Select Workspace')
        self.select_button.clicked.connect(self.select_workspace)
        self.select_button.setStyleSheet("background-color: #dcdcdc; border-radius: 5px;")
        file_layout.addWidget(self.select_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_directory)
        self.refresh_button.setStyleSheet("background-color: #dcdcdc;")
        file_layout.addWidget(self.refresh_button)

        main_layout.addWidget(file_frame)

        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget { background-color: #E0FFFF; border-radius: 5px; margin-top: 5px; }
            QTableWidget::item:selected { background-color: #e1d5e7; color: black; }
            QHeaderView::section { background-color: #b4a7d6; color: white; font-weight: bold; }
        """)
        self.table_widget.cellDoubleClicked.connect(self.cell_double_clicked)
        main_layout.addWidget(self.table_widget)

        self.load_directory('')
        self.folder_path = ''

        self.file_double_clicked.connect(self.handle_file_double_clicked)

    def load_directory(self, dir_path):
        if dir_path:
            folder_contents = list_folders_and_files(dir_path)
            self.folder_path = dir_path
            file_groups = group_files_by_prefix(folder_contents)
            table_data = create_table_data(file_groups)
            self.display_table(table_data)
            self.file_entry.setText(dir_path)
            self.populate_table_from_bf_file(file_groups)
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
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
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
        if row == 0:
            # Handle the first row (main file information)
            folder_name = self.table_widget.horizontalHeaderItem(column).text()
            file_name_item = self.table_widget.item(row, column)
            if file_name_item:
                file_name = file_name_item.text()
                if file_name:
                    file_path = os.path.join(self.folder_path, folder_name, file_name)
                    print(f"Opening file: {file_path}")
                    if os.path.exists(file_path):
                        self.file_double_clicked.emit(file_path)
                    else:
                        print(f"File not found: {file_path}")
        else:
            # Handle rows after the first row
            if column == 0:  # RDF_UI column
                ui_filename = self.table_widget.item(row, column).text()
                ui_file_path = os.path.join(self.folder_path, 'RDF_UI', ui_filename)
                print(f"Opening file: {ui_file_path}")
                if os.path.exists(ui_file_path):
                    self.file_double_clicked.emit(ui_file_path)
                else:
                    print(f"File not found: {ui_file_path}")
            elif column == 1:  # RDF_JS_OBJ column
                js_filename = self.table_widget.item(row, column).text()
                js_file_path = os.path.join(self.folder_path, 'RDF_JS_OBJ', js_filename)
                print(f"Opening file: {js_file_path}")
                if os.path.exists(js_file_path):
                    self.file_double_clicked.emit(js_file_path)
                else:
                    print(f"File not found: {js_file_path}")
            elif column == 2:  # RDF_BF column
                bf_filename = self.table_widget.item(row, column).text()
                bf_file_path = os.path.join(self.folder_path, 'RDF_BF', bf_filename)
                print(f"Opening file: {bf_file_path}")
                if os.path.exists(bf_file_path):
                    self.file_double_clicked.emit(bf_file_path)
                else:
                    print(f"File not found: {bf_file_path}")
            elif column == 3:  # RDF_BVO column
                bvo_filename = self.table_widget.item(row, column).text()
                bvo_file_path = os.path.join(self.folder_path, 'RDF_BVO', bvo_filename)
                print(f"Opening file: {bvo_file_path}")
                if os.path.exists(bvo_file_path):
                    self.file_double_clicked.emit(bvo_file_path)
                else:
                    print(f"File not found: {bvo_file_path}")
            elif column == 4:  # RDF_JSON column
                json_filename = self.table_widget.item(row, column).text()
                json_file_path = os.path.join(self.folder_path, 'RDF_JSON', json_filename)
                print(f"Opening file: {json_file_path}")
                if os.path.exists(json_file_path):
                    self.file_double_clicked.emit(json_file_path)
                else:
                    print(f"File not found: {json_file_path}")

    def handle_file_double_clicked(self, file_path):
        print(f"File double-clicked: {file_path}")

    def populate_table_from_bf_file(self, file_groups):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        try:
            # Get the BF file path from the first row's RDF_BF cell
            bf_file_path = os.path.join(self.folder_path, 'RDF_BF', self.table_widget.item(0, 2).text())

            if bf_file_path:
                logging.info(f"Reading BF file: {bf_file_path}")
                with open(bf_file_path, 'r') as file:
                    bf_code = file.read()

                ui_links = re.findall(r'(\w+UI)', bf_code)
                logging.info(f"Found {len(ui_links)} occurrences of text ending with 'UI' in {bf_file_path}")

                for ui_link in ui_links:
                    found_text = ui_link
                    logging.info(f"Found text: {found_text}")
                    ui_filename = found_text + '.php'
                    ui_file_path = os.path.join(self.folder_path, 'RDF_UI', ui_filename)
                    if os.path.exists(ui_file_path):
                        logging.info(f"Found UI file: {ui_file_path}")
                        prefix = ui_filename.split('UI')[0]
                        bf_filename = prefix + 'BF.php'
                        bf_file_path = os.path.join(self.folder_path, 'RDF_BF', bf_filename)
                        row_data = [
                            ui_filename,
                            prefix + 'Action.js',
                            bf_filename,
                            prefix + 'BVO.php',
                            prefix + 'Data.json'
                        ]
                        self.table_widget.insertRow(1)  # Insert the new row after the first row
                        for col_idx, cell_data in enumerate(row_data):
                            item = QTableWidgetItem(cell_data)
                            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                            self.table_widget.setItem(1, col_idx, item)
                    else:
                        logging.warning(f"UI file not found: {ui_file_path}")
            else:
                logging.warning("No BF file found in the selected directory")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

# If this script is run directly, create a QApplication and show the ProjectView window
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ProjectView()
    window.show()
    sys.exit(app.exec())
