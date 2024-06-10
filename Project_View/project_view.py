import os
import re
import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QTableWidget,
                             QTableWidgetItem, QPushButton, QFrame, QHeaderView, QLabel)
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
                file_groups[prefix] = {'RDF_UI': None, 'RDF_ACTION': None, 'RDF_BW': None, 'RDF_BVO': None, 'RDF_DATA': None}
            if 'BW' in file_name:
                file_groups[prefix]['RDF_BW'] = file_name
            elif 'BVO' in file_name:
                file_groups[prefix]['RDF_BVO'] = file_name
            elif 'Data' in file_name:
                file_groups[prefix]['RDF_DATA'] = file_name
            elif 'Action' in file_name:
                file_groups[prefix]['RDF_ACTION'] = file_name
            elif 'UI' in file_name:
                file_groups[prefix]['RDF_UI'] = file_name
    return file_groups

def create_table_data(file_groups):
    with open('readme.txt', 'r') as file:
        main_file = file.read().split(':')[1].strip()

    columns = ['RDF_UI', 'RDF_ACTION', 'RDF_BW', 'RDF_BVO', 'RDF_DATA']
    rows = []
    main_file_group = {'RDF_UI': main_file, 'RDF_ACTION': None, 'RDF_BW': None, 'RDF_BVO': None, 'RDF_DATA': None}

    for prefix, file_group in file_groups.items():
        if file_group['RDF_UI'] == main_file:
            main_file_group.update(file_group)
            break

    for _, file_group in file_groups.items():
        rows.append([file_group['RDF_UI'], file_group['RDF_ACTION'], file_group['RDF_BW'], file_group['RDF_BVO'], file_group['RDF_DATA']])

    table_data = [columns, list(main_file_group.values())] + rows
    return table_data

def get_prefix(filename):
    return filename.split('BW')[0] if 'BW' in filename else \
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
        file_frame.setStyleSheet("background-color: #232228; border-radius: 10px; height: 20px; padding: 2px;")
        file_layout = QHBoxLayout(file_frame)

        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Selected Directory")
        self.file_entry.setReadOnly(True)
        self.file_entry.setStyleSheet("border-radius: 5px; color: #fcfcfc;")
        file_layout.addWidget(self.file_entry)

        self.select_button = QPushButton('Select Workspace')
        self.select_button.clicked.connect(self.select_workspace)
        self.select_button.setStyleSheet("background-color: #323234; border-radius: 5px;padding: 5px;color: #fcfcfc;")
        file_layout.addWidget(self.select_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_directory)
        self.refresh_button.setStyleSheet("background-color: #323234;border-radius: 5px; padding: 5px; color: #fcfcfc;")
        file_layout.addWidget(self.refresh_button)

        self.merge_button = QPushButton('Merge')
        self.merge_button.clicked.connect(self.merge_files)
        self.merge_button.setStyleSheet("background-color: #323234;border-radius: 5px; padding: 5px; color: #fcfcfc;")
        file_layout.addWidget(self.merge_button)

        main_layout.addWidget(file_frame)

        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget { background-color: #ffffff; border-radius: 10px; margin-top: 5px; padding: 10px;}
            QTableWidget::item:selected { background-color: #fdfdfd; color: black; }
            QHeaderView::section { background-color: #7657ff; color: black; font-weight: bold; }
            QTableWidget::item { border-radius: 10px; }
        """)
        self.table_widget.cellDoubleClicked.connect(self.cell_double_clicked)
        main_layout.addWidget(self.table_widget)

        unlinked_files_label = QLabel("Unlinked Files")
        unlinked_files_label.setStyleSheet("background-color: #232228;color: #f3f3f3; padding: 5px; border-radius: 10px; text-align: center; item-align: center; qproperty-alignment: AlignCenter; font-weight: bold;")
        main_layout.addWidget(unlinked_files_label)

        self.unlinked_table_widget = QTableWidget()
        self.unlinked_table_widget.setStyleSheet("""
            QTableWidget { background-color: #ffffff; border-radius: 10px; margin-top: 5px; padding: 10px;}
            QTableWidget::item:selected { background-color: #fdfdfd; color: black; }
            QHeaderView::section { background-color: #7657ff; color: black; font-weight: bold; }
            QTableWidget::item { border-radius: 10px; }
        """)
        main_layout.addWidget(self.unlinked_table_widget)

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
            self.populate_table_from_bw_file(file_groups)

            # Collect all file paths in the directory
            all_file_paths = set()
            for folder_name, files in folder_contents.items():
                for file_name in files:
                    file_path = os.path.join(self.folder_path, folder_name, file_name)
                    all_file_paths.add(file_path)

            # Collect file paths from the main table
            displayed_file_paths = set()
            for row in range(1, self.table_widget.rowCount()):  # Start from row 1 to skip the header
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item:
                        file_name = item.text()
                        if file_name:
                            folder_name = self.table_widget.horizontalHeaderItem(col).text()
                            file_path = os.path.join(self.folder_path, folder_name, file_name)
                            displayed_file_paths.add(file_path)

            # Find undisplayed file paths
            undisplayed_file_paths = list(all_file_paths - displayed_file_paths)
            self.display_unlinked_files(undisplayed_file_paths)
        else:
            self.file_entry.setText("Selected Directory")

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

    def display_unlinked_files(self, undisplayed_file_paths):
        self.unlinked_table_widget.clear()

        # Extract folder names from undisplayed file paths
        folders = sorted(set(os.path.basename(os.path.dirname(path)) for path in undisplayed_file_paths))
        self.unlinked_table_widget.setColumnCount(len(folders))
        self.unlinked_table_widget.setHorizontalHeaderLabels(folders)

        files_by_folder = {folder: [] for folder in folders}
        for file_path in undisplayed_file_paths:
            folder_name = os.path.basename(os.path.dirname(file_path))
            files_by_folder[folder_name].append(file_path)

        # Find the maximum number of files in any folder to determine the row count
        max_files_count = max(len(files) for files in files_by_folder.values())
        self.unlinked_table_widget.setRowCount(max_files_count)

        for col_idx, folder_name in enumerate(folders):
            for row_idx, file_path in enumerate(files_by_folder[folder_name]):
                item = QTableWidgetItem(os.path.basename(file_path))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.unlinked_table_widget.setItem(row_idx, col_idx, item)

        self.unlinked_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def select_workspace(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.load_directory(dir_path)

    def refresh_directory(self):
        if self.folder_path:
            self.load_directory(self.folder_path)
        else:
            self.file_entry.setText("Please select a directory first")

    def cell_double_clicked(self, row, column):
        if row == 0:
            folder_name_item = self.table_widget.horizontalHeaderItem(column)
            file_name_item = self.table_widget.item(row, column)
            if folder_name_item and file_name_item:
                folder_name = folder_name_item.text()
                file_name = file_name_item.text()
                if file_name:
                    file_path = os.path.join(self.folder_path, folder_name, file_name)
                    if os.path.exists(file_path):
                        self.file_double_clicked.emit(file_path)
        else:
            column_map = {0: 'RDF_UI', 1: 'RDF_ACTION', 2: 'RDF_BW', 3: 'RDF_BVO', 4: 'RDF_DATA'}
            folder_name = column_map.get(column)
            if folder_name:
                file_name = self.table_widget.item(row, column).text()
                if file_name:
                    file_path = os.path.join(self.folder_path, folder_name, file_name)
                    if os.path.exists(file_path):
                        self.file_double_clicked.emit(file_path)

    def handle_file_double_clicked(self, file_path):
        print(f"File double-clicked: {file_path}")

    def merge_files(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Files (*.php *.js *.json)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.add_to_unlinked_table(selected_files)

    def add_to_unlinked_table(self, file_paths):
        existing_columns = [self.unlinked_table_widget.horizontalHeaderItem(i).text() for i in range(self.unlinked_table_widget.columnCount())]
        new_file_dict = {}
        for file_path in file_paths:
            folder_name = os.path.basename(os.path.dirname(file_path))
            file_name = os.path.basename(file_path)
            if folder_name not in new_file_dict:
                new_file_dict[folder_name] = []
            new_file_dict[folder_name].append(file_name)

        for folder_name, files in new_file_dict.items():
            if folder_name not in existing_columns:
                self.unlinked_table_widget.insertColumn(len(existing_columns))
                self.unlinked_table_widget.setHorizontalHeaderItem(len(existing_columns), QTableWidgetItem(folder_name))
                existing_columns.append(folder_name)
            col_idx = existing_columns.index(folder_name)
            for file_name in files:
                row_idx = self.unlinked_table_widget.rowCount()
                self.unlinked_table_widget.insertRow(row_idx)
                item = QTableWidgetItem(file_name)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.unlinked_table_widget.setItem(row_idx, col_idx, item)

        self.unlinked_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def populate_table_from_bw_file(self, file_groups):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        try:
            # Get the BW file path from the first row's RDF_BW cell
            bw_file_path = os.path.join(self.folder_path, 'RDF_BW', self.table_widget.item(0, 2).text())

            if bw_file_path:
                logging.info(f"Reading BW file: {bw_file_path}")
                with open(bw_file_path, 'r') as file:
                    bw_code = file.read()

                ui_links = re.findall(r'(\w+UI)', bw_code)
                logging.info(f"Found {len(ui_links)} occurrences of text ending with 'UI' in {bw_file_path}")

                # Clear existing rows (except the first row)
                self.table_widget.setRowCount(1)

                for ui_link in ui_links:
                    found_text = ui_link
                    logging.info(f"Found text: {found_text}")
                    ui_filename = found_text + '.php'
                    ui_file_path = os.path.join(self.folder_path, 'RDF_UI', ui_filename)
                    if os.path.exists(ui_file_path):
                        logging.info(f"Found UI file: {ui_file_path}")
                        prefix = ui_filename.split('UI')[0]
                        bw_filename = prefix + 'BW.php'
                        bw_file_path = os.path.join(self.folder_path, 'RDF_BW', bw_filename)
                        row_data = [
                            ui_filename,
                            prefix + 'Action.js',
                            bw_filename,
                            prefix + 'BVO.php',
                            prefix + 'Data.json'
                        ]

                        # Skip adding a new row if the UI file is the main file
                        if ui_filename == self.table_widget.item(0, 0).text():
                            continue

                        row_position = self.table_widget.rowCount()
                        self.table_widget.insertRow(row_position)
                        for col_idx, cell_data in enumerate(row_data):
                            item = QTableWidgetItem(cell_data)
                            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                            self.table_widget.setItem(row_position, col_idx, item)
                    else:
                        logging.warning(f"UI file not found: {ui_file_path}")
            else:
                logging.warning("No BW file found in the selected directory")
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
