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

            # Get a list of all file paths in the directory
            all_file_paths = []
            for folder_name, files in folder_contents.items():
                for file_name in files:
                    file_path = os.path.join(self.folder_path, folder_name, file_name)
                    all_file_paths.append(file_path)

            # Get a set of displayed file paths from the main table
            displayed_file_paths = set()
            for row_data in table_data[1:]:
                for file_path in row_data:
                    if file_path:
                        displayed_file_paths.add(os.path.join(self.folder_path, *file_path.split('/')))

            # Remove displayed file paths from the list of all file paths
            undisplayed_file_paths = [file_path for file_path in all_file_paths if file_path not in displayed_file_paths]

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
        self.unlinked_table_widget.setColumnCount(1)
        self.unlinked_table_widget.setHorizontalHeaderLabels(["Undisplayed Files"])
        self.unlinked_table_widget.setRowCount(len(undisplayed_file_paths))

        for row_idx, file_path in enumerate(undisplayed_file_paths):
            item = QTableWidgetItem(file_path)
            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.unlinked_table_widget.setItem(row_idx, 0, item)

        self.unlinked_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def select_workspace(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.load_directory(dir_path)

    def refresh_directory(self):
        if self.folder_path:
            self.load_directory(self.folder_path)
        else:
            self.file_entry.setText("Selected Directory")

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
            elif column == 1:  # RDF_ACTION column
                js_filename = self.table_widget.item(row, column).text()
                js_file_path = os.path.join(self.folder_path, 'RDF_ACTION', js_filename)
                print(f"Opening file: {js_file_path}")
                if os.path.exists(js_file_path):
                    self.file_double_clicked.emit(js_file_path)
                else:
                    print(f"File not found: {js_file_path}")
            elif column == 2:  # RDF_BW column
                bw_filename = self.table_widget.item(row, column).text()
                bw_file_path = os.path.join(self.folder_path, 'RDF_BW', bw_filename)
                print(f"Opening file: {bw_file_path}")
                if os.path.exists(bw_file_path):
                    self.file_double_clicked.emit(bw_file_path)
                else:
                    print(f"File not found: {bw_file_path}")
            elif column == 3:  # RDF_BVO column
                bvo_filename = self.table_widget.item(row, column).text()
                bvo_file_path = os.path.join(self.folder_path, 'RDF_BVO', bvo_filename)
                print(f"Opening file: {bvo_file_path}")
                if os.path.exists(bvo_file_path):
                    self.file_double_clicked.emit(bvo_file_path)
                else:
                    print(f"File not found: {bvo_file_path}")
            elif column == 4:  # RDF_DATA column
                json_filename = self.table_widget.item(row, column).text()
                json_file_path = os.path.join(self.folder_path, 'RDF_DATA', json_filename)
                print(f"Opening file: {json_file_path}")
                if os.path.exists(json_file_path):
                    self.file_double_clicked.emit(json_file_path)
                else:
                    print(f"File not found: {json_file_path}")
    def handle_file_double_clicked(self, file_path):
        print(f"File double-clicked: {file_path}")

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