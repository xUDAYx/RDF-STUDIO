import sys,os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import QProcess, Qt
from Project_View.project_view import ProjectView
from UI_Code_Editor.php_editor import PhpEditor
from JS_Lib_Editor.js_editor import JsEditor
from Biz_Func_Editor.php_editor import PhpEditorBF
from JSON_Editor.json_editor import JsonEditor
from BVO_Editor.bvo_editor import BVOEditor
from Theme.colors import Colors
from PyQt6.QtGui import QIcon
import sys
import traceback
import logging
cwd = os.getcwd()

logging.basicConfig(filename='error.log', level=logging.ERROR)

def excepthook(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Install the custom exception handler
sys.excepthook = excepthook
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.colors = Colors()

        self.setWindowTitle("RDF Studio | Python | Generative AI")
        self.showMaximized()
        self.setStyleSheet(f"background-color: {self.colors.background_color};")
        self.setWindowFlags(Qt.WindowType.Window)
        

        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)  # Use QVBoxLayout to stack navbar and content

        # Navbar widget with grey background
        navbar_widget = QWidget()
        navbar_widget.setFixedHeight(60)
        navbar_widget.setStyleSheet(f"background-color: {self.colors.navbar_color};border-radius: 10px;")
        top_layout = QHBoxLayout(navbar_widget)


        # List of icon file names (replace with your actual icon file names)
        icon_file_names = ["home.png", "save.png", "code_1.png"]

        icon_paths = [os.path.join(cwd, "Theme", "icons", icon_file_name) for icon_file_name in icon_file_names]

        self.button_1 = QPushButton()
        self.button_1.setFixedSize(40, 40)
        self.button_1.setIcon(QIcon(icon_paths[0]))
        self.button_1.setStyleSheet("background-color: #323234; border: none; border-radius: 10px; padding: 5px;")
        top_layout.addWidget(self.button_1)
        for i, icon_path in enumerate(icon_paths[1:], start=1):
            button = QPushButton()
            button.setFixedSize(40, 40)
            button.setIcon(QIcon(icon_path))
            button.setStyleSheet(f"background-color: {self.colors.button_colors[i]}; border: none; border-radius: 10px;")
            top_layout.addWidget(button)

        search_bar_nav = QLineEdit()
        search_bar_nav.setPlaceholderText("Search")
        search_bar_nav.setFixedHeight(40)
        search_bar_nav.setStyleSheet("background-color: #323234; color:  #fcfcfc; border-radius: 10px; padding: 5px 5px 5px 10px; margin-left: 400px;")
        top_layout.addWidget(search_bar_nav)

        main_layout.addWidget(navbar_widget)

        # Main content area with sidebar and content
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)

        # Left layout for sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet(f"background-color: {self.colors.sidebar_color}; border-radius: 10px;")

        self.sidebar_buttons = {}
        sidebar_items = [
            "Project View",
            "UI Code Editor",
            "JS Editor",
            "Business Func Editor",
            "BVO Editor",
            "JSON Editor"
            
        ]

        for item in sidebar_items:
            button = QPushButton(item)
            button.setFixedHeight(40)
            button.setStyleSheet(f"""
                color: #fcfcfc;
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: {self.colors.sidebar_button_color};
            """)
            button.clicked.connect(lambda checked, b=item: self.sidebar_button_clicked(b))
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(5)
            self.sidebar_buttons[item] = button

        # Add "Restart" button at the bottom
        restart_button = QPushButton("Restart")
        restart_button.setFixedHeight(40)
        restart_button.setStyleSheet(f"""
            color: #fcfcfc;
            font-size: 16px;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            background-color: {self.colors.sidebar_button_color};
        """)
        restart_button.clicked.connect(self.restart_application)
        sidebar_layout.addStretch(1)  # Add stretch to push the button to the bottom
        sidebar_layout.addWidget(restart_button)

        content_layout.addWidget(sidebar_widget)

        # Right layout for main content
        self.right_layout = QVBoxLayout()
        content_layout.addLayout(self.right_layout)
        main_layout.addWidget(content_widget)

        self.setCentralWidget(main_widget)

        self.project_view_instance = None
        self.html_editor_instance = None
        self.js_editor_instance = None
        self.biz_func_editor_instance = None
        self.json_editor_instance = None
        self.bvo_editor_instance = None
        self.current_button = None

        self.sidebar_button_clicked("Project View")

    def sidebar_button_clicked(self, button_name):
        if self.current_button:
            self.current_button.setStyleSheet(f"""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                color: black;
                text-align: center;
                background-color: {self.colors.sidebar_button_color};
            """)
        
        if button_name == "Project View":
            self.load_project_view()
        elif button_name == "UI Code Editor":
            self.load_ui_code_editor()
        elif button_name == "JS Editor":
            self.load_js_lib_editor()
        elif button_name == "Business Func Editor":
            self.load_biz_func_editor()
        elif button_name == "JSON Editor":
            self.load_json_editor()
        elif button_name == "BVO Editor":
            self.load_bvo_editor()
        

        self.current_button = self.sidebar_buttons[button_name]
        self.current_button.setStyleSheet(f"""
            font-size: 16px;
            border-radius: 10px;
            padding: 5px;
                                          color:  #fcfcfc;
            text-align: center;
            background-color: {self.colors.sidebar_button_selected_color};
        """)

    def update_selected_button(self, button_name):
        if self.current_button:
            self.current_button.setStyleSheet(f"""
                color:  #fcfcfc;
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;                           
                background-color: {self.colors.sidebar_button_color};
            """)
        
        self.current_button = self.sidebar_buttons[button_name]
        self.current_button.setStyleSheet(f"""
            font-size: 16px;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            background-color: {self.colors.sidebar_button_selected_color};
        """)

    def load_project_view(self):
        if not self.project_view_instance:
            self.project_view_instance = ProjectView()
            self.project_view_instance.file_double_clicked.connect(self.open_file_in_editor)
        self.display_content(self.project_view_instance)
        self.update_selected_button("Project View")

    def load_ui_code_editor(self):
        if not self.html_editor_instance:
            self.html_editor_instance = PhpEditor()
        self.display_content(self.html_editor_instance)
        self.update_selected_button("UI Code Editor")

    def load_js_lib_editor(self):
        if not self.js_editor_instance:
            self.js_editor_instance = JsEditor()
        self.display_content(self.js_editor_instance)
        self.update_selected_button("JS Editor")

    def load_biz_func_editor(self):
        if not self.biz_func_editor_instance:
            self.biz_func_editor_instance = PhpEditorBF()
        self.display_content(self.biz_func_editor_instance)
        self.update_selected_button("Business Func Editor")
    
    def load_json_editor(self):
        if not self.json_editor_instance:
            self.json_editor_instance = JsonEditor()
        self.display_content(self.json_editor_instance)
        self.update_selected_button("JSON Editor")
    
    def load_bvo_editor(self):
        if not self.bvo_editor_instance:
            self.bvo_editor_instance = BVOEditor()
        self.display_content(self.bvo_editor_instance)
        self.update_selected_button("BVO Editor")

    def display_content(self, widget):
        # Clear the existing layout
        for i in reversed(range(self.right_layout.count())):
            widget_to_remove = self.right_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        
        # Add the new widget
        self.right_layout.addWidget(widget)

    def open_file_in_editor(self, file_path):
        if "RDF_UI" in file_path:
            if not self.html_editor_instance:
                self.html_editor_instance = PhpEditor()
            self.load_ui_code_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.html_editor_instance.set_code(code)
            self.update_selected_button("UI Code Editor")
            
        if "RDF_ACTION" in file_path:
            if not self.js_editor_instance:
                self.js_editor_instance = JsEditor()
            self.load_js_lib_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.js_editor_instance.set_code(code)
            self.update_selected_button("JS Editor")
            
        if "RDF_BW" in file_path:
            if not self.biz_func_editor_instance:
                self.biz_func_editor_instance = PhpEditorBF()
            self.load_biz_func_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.biz_func_editor_instance.set_code(code)
            self.update_selected_button("Business Func Editor")
        
        if "RDF_DATA" in file_path:
                if not self.json_editor_instance:
                    self.json_editor_instance = JsonEditor()
                self.load_json_editor()
                with open(file_path, 'r') as file:
                    json_code = file.read()
                self.json_editor_instance.set_code(json_code)
                self.update_selected_button("JSON Editor")
                
        
        if "RDF_BVO" in file_path:
            if not self.bvo_editor_instance:
                self.bvo_editor_instance = BVOEditor()
            self.load_bvo_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.bvo_editor_instance.set_code(code)
            self.update_selected_button("BVO Editor")
        else:
            pass

    def run_code(self):
        if self.current_button == self.sidebar_buttons["UI Code Editor"]:
            if self.html_editor_instance:
                self.html_editor_instance.run_php()
        if self.current_button == self.sidebar_buttons["JS Editor"]:
            if self.js_editor_instance:
                self.js_editor_instance.run_js()
        if self.current_button == self.sidebar_buttons["Business Func Editor"]:
            if self.biz_func_editor_instance:
                self.biz_func_editor_instance.run_php1()
        if self.current_button == self.sidebar_buttons["JSON Editor"]:
            if self.json_editor_instance:
                self.json_editor_instance.run_json()
        if self.current_button == self.sidebar_buttons["BVO Editor"]:
            if self.bvo_editor_instance:
                self.bvo_editor_instance.run_bvo()

    def restart_application(self):
        # Restart the application
        qapp = QApplication.instance()
        qapp.quit()
        QProcess.startDetached(sys.executable, sys.argv)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
