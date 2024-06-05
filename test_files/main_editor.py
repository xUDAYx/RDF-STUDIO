# main_window.py
import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog,
                             QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMainWindow, QFrame, QStackedWidget, QTextEdit)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt
from html_editor import HtmlEditor


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

        self.setWindowTitle("RDF Studio | Python | Generative AI")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: pink;")

        # Main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet("background-color: #F0F0F0; border-radius: 10px;")

        sidebar_items = [
            "Project View",
            "UI Designer",
            "UI Code Editor",
            "JavaScript Editor",
            "Web part Editor",
            "Business Workflow Editor",
            "Com' Func' Editor",
            "BVO Editor",
            "JSON Editor"
        ]

        self.stack = QStackedWidget()
        self.editor_widgets = {}
        self.sidebar_buttons = {}

        for item in sidebar_items:
            button = QPushButton(item)
            button.setFixedHeight(40)
            button.setStyleSheet("""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #E0E0E0;
            """)
            button.clicked.connect(lambda checked, item=item: self.display_editor(item))
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(5)

            self.sidebar_buttons[item] = button

            if item == "Project View":
                # Project View widget
                project_view_widget = QWidget()
                project_view_layout = QVBoxLayout(project_view_widget)

                # Top layout for colored buttons and search bar
                top_layout = QHBoxLayout()

                pastel_colors = [
                    "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
                    "#B4A7D6", "#D5A6BD", "#A9D18E", "#D5E8D4", "#E1D5E7", "#FFF2CC"
                ]

                # Add the play button as the 1st button on the left side of the navbar
                play_button = QPushButton()
                play_button.setFixedSize(40, 40)
                play_button.setStyleSheet("""
                    background-color: #FFFFFF; 
                    border: none; 
                    border-radius: 10px;
                """)
                # You need to provide a path to your icon file or comment out this line if you don't have it
                play_button.setIcon(QIcon("download (1).jpeg.png"))
                top_layout.addWidget(play_button)

                # Add 11 colored buttons to the left side of the navbar
                for color in pastel_colors:
                    btn = QPushButton()
                    btn.setFixedSize(40, 40)
                    btn.setStyleSheet(f"background-color: {color}; border: none; border-radius: 10px;")
                    top_layout.addWidget(btn)

                search_bar_nav = QLineEdit()
                search_bar_nav.setPlaceholderText("Search")
                search_bar_nav.setFixedHeight(40)
                search_bar_nav.setStyleSheet("background-color: white; border-radius: 10px; padding: 5px;")
                top_layout.addWidget(search_bar_nav)

                project_view_layout.addLayout(top_layout)

                # Adding image
                self.image_label = QLabel()
                self.image_label.setPixmap(QPixmap("/mnt/data/image.png"))
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                project_view_layout.addWidget(self.image_label)

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

                project_view_layout.addWidget(file_frame)

                # Table widget
                self.table_widget = QTableWidget()
                self.table_widget.setStyleSheet("""
                    QTableWidget { background-color: #E0FFFF; }
                    QTableWidget::item:selected { background-color: #FFA07A; color: black; }
                    QHeaderView::section { background-color: #FF4500; color: white; font-weight: bold; }
                """)
                self.table_widget.cellClicked.connect(self.cell_clicked)
                self.table_widget.cellDoubleClicked.connect(self.cell_double_clicked)
                project_view_layout.addWidget(self.table_widget)

                self.editor_widgets[item] = project_view_widget
                self.stack.addWidget(project_view_widget)
            elif item == "UI Code Editor":
                # UI Designer widget with color buttons and search input on top, and HTML editor below
                ui_designer_widget = QWidget()
                ui_designer_layout = QVBoxLayout(ui_designer_widget)

                # Top layout for colored buttons and search bar
                top_layout = QHBoxLayout()

                # Add the play button as the 1st button on the left side of the navbar
                play_button = QPushButton()
                play_button.setFixedSize(40, 40)
                play_button.setStyleSheet("""
                    background-color: #FFFFFF; 
                    border: none; 
                    border-radius: 10px;
                """)
                # You need to provide a path to your icon file or comment out this line if you don't have it
                play_button.setIcon(QIcon("download (1).jpeg.png"))
                top_layout.addWidget(play_button)

                # Add 11 colored buttons to the left side of the navbar
                for color in pastel_colors:
                    btn = QPushButton()
                    btn.setFixedSize(40, 40)
                    btn.setStyleSheet(f"background-color: {color}; border: none; border-radius: 10px;")
                    top_layout.addWidget(btn)

                search_bar_nav = QLineEdit()
                search_bar_nav.setPlaceholderText("Search")
                search_bar_nav.setFixedHeight(40)
                search_bar_nav.setStyleSheet("background-color: white; border-radius: 10px; padding: 5px;")
                top_layout.addWidget(search_bar_nav)

                ui_designer_layout.addLayout(top_layout)

                # Add HTML editor
                html_editor_widget = HtmlEditor()
                ui_designer_layout.addWidget(html_editor_widget)

                self.editor_widgets[item] = ui_designer_widget
                self.stack.addWidget(ui_designer_widget)
            else:
                editor = QTextEdit()
                editor.setStyleSheet("background-color: #FFFFFF;")
                self.editor_widgets[item] = editor
                self.stack.addWidget(editor)

        # Ensure the Project View button is highlighted and selected by default
        self.display_editor("Project View")

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

        self.load_directory('D:/migration_campus')

    def display_editor(self, editor_name):
        self.stack.setCurrentWidget(self.editor_widgets[editor_name])
        for name, button in self.sidebar_buttons.items():
            if name == editor_name:
                button.setStyleSheet("""
                    font-size: 16px;
                    border-radius: 10px;
                    padding: 5px;
                    text-align: center;
                    background-color: pink;
                """)
            else:
                button.setStyleSheet("""
                    font-size: 16px;
                    border-radius: 10px;
                    padding: 5px;
                    text-align: center;
                    background-color: #E0E0E0;
                """)

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

    def cell_clicked(self, row, column):
        item = self.table_widget.item(row, column)
        if item and item.text():
            filename = item.text()
            self.display_filename_window(filename)

    def cell_double_clicked(self, row, column):
        item = self.table_widget.item(row, column)
        if item and item.text():
            filename = item.text()
            folder_name = self.file_entry.text()
            if folder_name.endswith("RDF_UI") and os.path.isfile(os.path.join(folder_name, filename)):
                # Load content of the file into the HTML editor
                file_path = os.path.join(folder_name, filename)
                with open(file_path, 'r') as file:
                    html_code = file.read()
                    self.editor_widgets["UI Code Editor"].editor.setPlainText(html_code)
                self.display_editor("UI Code Editor")
            else:
                self.open_file_in_new_tab(filename)


    def display_filename_window(self, filename):
        new_window = QWidget()
        new_window.setWindowTitle('File Selected')
        layout = QVBoxLayout(new_window)
        label = QLabel(filename)
        label.setFont(QFont('Arial', 16))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        new_window.resize(300, 200)
        new_window.show()

    def open_file_in_new_tab(self, filename):
        print(f"Opening file: {filename}")  # Debug statement
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        label = QLabel(filename)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        new_tab.setLayout(layout)
        tab_title = filename if filename else "Untitled"
        self.stack.addWidget(new_tab)
        self.stack.setCurrentWidget(new_tab)
        print(f"New tab added with title: {tab_title}")  # Debug statement

    def display_error_window(self, message):
        new_window = QWidget()
        new_window.setWindowTitle('Error')
        layout = QVBoxLayout(new_window)
        label = QLabel(message)
        label.setFont(QFont('Arial', 16))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        new_window.resize(300, 200)
        new_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
