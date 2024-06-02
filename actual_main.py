import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from Project_View.project_view import ProjectView  # Import the ProjectView class
from UI_Code_Editor.php_editor import PhpEditor  # Import the PhpEditor class
from JS_Lib_Editor.js_editor import JsEditor  # Import the JsEditor class
from Biz_Func_Editor.php_editor import PhpEditorBF #Import the PhpEditorBF
from JSON_Editor.json_editor import JsonEditor
from BVO_Editor.bvo_editor import BVOEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RDF Studio | Python | Generative AI")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: pink;")

        # Main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)  # Use QHBoxLayout for sidebar and main content

        # Left layout for sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet("background-color: #F0F0F0; border-radius: 10px;")

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
            button.setStyleSheet("""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #E0E0E0;
            """)
            button.clicked.connect(lambda checked, b=item: self.sidebar_button_clicked(b))
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(5)
            self.sidebar_buttons[item] = button

        sidebar_layout.addStretch(1)
        main_layout.addWidget(sidebar_widget)

        # Right layout for main content
        self.right_layout = QVBoxLayout()
        
        # Top layout for colored buttons and search bar
        top_layout = QHBoxLayout()

        # Add 11 colored buttons to the left side of the navbar
        self.button_1 = QPushButton()
        self.button_1.setFixedSize(40, 40)
        self.button_1.setText("▶️")
        self.button_1.setStyleSheet("background-color: #FFB3BA; border: none; border-radius: 10px;border: 1px solid black;border-radius: 3px; padding: 5px; ")
        #button_1.clicked.connect(self.run_html)
        top_layout.addWidget(self.button_1)

        button_2 = QPushButton()
        button_2.setFixedSize(40, 40)
        button_2.setStyleSheet("background-color: #FFDFBA; border: none; border-radius: 10px;")
        top_layout.addWidget(button_2)

        button_3 = QPushButton()
        button_3.setFixedSize(40, 40)
        button_3.setStyleSheet("background-color: #FFFFBA; border: none; border-radius: 10px;")
        top_layout.addWidget(button_3)

        button_4 = QPushButton()
        button_4.setFixedSize(40, 40)
        button_4.setStyleSheet("background-color: #BAFFC9; border: none; border-radius: 10px;")
        top_layout.addWidget(button_4)

        button_5 = QPushButton()
        button_5.setFixedSize(40, 40)
        button_5.setStyleSheet("background-color: #BAE1FF; border: none; border-radius: 10px;")
        top_layout.addWidget(button_5)

        button_6 = QPushButton()
        button_6.setFixedSize(40, 40)
        button_6.setStyleSheet("background-color: #B4A7D6; border: none; border-radius: 10px;")
        top_layout.addWidget(button_6)

        button_7 = QPushButton()
        button_7.setFixedSize(40, 40)
        button_7.setStyleSheet("background-color: #D5A6BD; border: none; border-radius: 10px;")
        top_layout.addWidget(button_7)

        button_8 = QPushButton()
        button_8.setFixedSize(40, 40)
        button_8.setStyleSheet("background-color: #A9D18E; border: none; border-radius: 10px;")
        top_layout.addWidget(button_8)

        button_9 = QPushButton()
        button_9.setFixedSize(40, 40)
        button_9.setStyleSheet("background-color: #D5E8D4; border: none; border-radius: 10px;")
        top_layout.addWidget(button_9)

        button_10 = QPushButton()
        button_10.setFixedSize(40, 40)
        button_10.setStyleSheet("background-color: #E1D5E7; border: none; border-radius: 10px;")
        top_layout.addWidget(button_10)

        button_11 = QPushButton()
        button_11.setFixedSize(40, 40)
        button_11.setStyleSheet("background-color: #FFF2CC; border: none; border-radius: 10px;")
        top_layout.addWidget(button_11)

        search_bar_nav = QLineEdit()
        search_bar_nav.setPlaceholderText("Search")
        search_bar_nav.setFixedHeight(40)
        search_bar_nav.setStyleSheet("background-color: white; border-radius: 10px; padding: 5px;")
        top_layout.addWidget(search_bar_nav)

        self.right_layout.addLayout(top_layout)

        # Add a placeholder for project view
        self.project_view_placeholder = QWidget()
        self.right_layout.addWidget(self.project_view_placeholder)

        main_layout.addLayout(self.right_layout)

        self.setCentralWidget(main_widget)

        self.project_view_instance = None
        self.html_editor_instance = None
        self.js_editor_instance = None
        self.biz_func_editor_instance = None
        self.json_editor_instance = None
        self.bvo_editor_instance = None
        self.current_button = None

        self.button_1.clicked.connect(self.run_code)

    def sidebar_button_clicked(self, button_name):
        if self.current_button:
            self.current_button.setStyleSheet("""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #E0E0E0;
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
        self.current_button.setStyleSheet("""
            font-size: 16px;
            border-radius: 10px;
            padding: 5px;
            text-align: center;
            background-color: pink;
        """)

    def update_sidebar_color(self, button_name):
        # Reset all sidebar button colors to default
        for button in self.sidebar_buttons.values():
            button.setStyleSheet("""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #E0E0E0;
            """)
        # Set the color of the specified sidebar button to pink
        if button_name in self.sidebar_buttons:
            self.sidebar_buttons[button_name].setStyleSheet("""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: pink;
            """)

    def load_project_view(self):
        if not self.project_view_instance:
            self.project_view_instance = ProjectView()
            self.project_view_instance.file_double_clicked.connect(self.open_file_in_editor)
        self.display_content(self.project_view_instance)

    def load_ui_code_editor(self):
        if not self.html_editor_instance:
            self.html_editor_instance = PhpEditor()
        self.display_content(self.html_editor_instance)

    def load_js_lib_editor(self):
        if not self.js_editor_instance:
            self.js_editor_instance = JsEditor()
        self.display_content(self.js_editor_instance)

    def load_biz_func_editor(self):
        if not self.biz_func_editor_instance:
            self.biz_func_editor_instance = PhpEditorBF()
        self.display_content(self.biz_func_editor_instance)
    
    def load_json_editor(self):
        if not self.json_editor_instance:
            self.json_editor_instance = JsonEditor()
        self.display_content(self.json_editor_instance)
    
    def load_bvo_editor(self):
        if not self.bvo_editor_instance:
            self.bvo_editor_instance = BVOEditor()
        self.display_content(self.bvo_editor_instance)

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
            self.update_sidebar_color("UI Code Editor")
            
        if "RDF_JS_OBJ" in file_path:
            if not self.js_editor_instance:
                self.js_editor_instance = JsEditor()
            self.load_js_lib_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.js_editor_instance.set_code(code)
            self.update_sidebar_color("JS Editor")
            
        if "RDF_BF" in file_path:
            if not self.biz_func_editor_instance:
                self.biz_func_editor_instance = PhpEditorBF()
            self.load_biz_func_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.biz_func_editor_instance.set_code(code)
            self.update_sidebar_color("Business Func Editor")
        
        if "RDF_JSON" in file_path:
            if not self.json_editor_instance:
                self.json_editor_instance = JsonEditor()
            self.load_json_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.json_editor_instance.set_code(code)
            self.update_sidebar_color("JSON Editor")
        
        if "RDF_BVO" in file_path:
            if not self.bvo_editor_instance:
                self.bvo_editor_instance = BVOEditor()
            self.load_bvo_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.bvo_editor_instance.set_code(code)
            self.update_sidebar_color("BVO Editor")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
