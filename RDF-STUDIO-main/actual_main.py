import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,QMessageBox
from Project_View.project_view import ProjectView  # Import the ProjectView class
from UI_Code_Editor.php_editor import PhpEditor  # Import the PhpEditor class
from JS_Lib_Editor.js_editor import JsEditor  # Import the JsEditor class
from Biz_Func_Editor.php_editor import PhpEditorBF  # Import the PhpEditorBF class
from JSON_Editor.json_editor import JsonEditor  # Import the JsonEditor class
from BVO_Editor.bvo_editor import BVOEditor  # Import the BVOEditor class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RDF Studio | Python | Generative AI")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: pink;")

        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)  # Use QVBoxLayout to stack navbar and content

        # Navbar widget with grey background
        navbar_widget = QWidget()
        navbar_widget.setFixedHeight(60)
        navbar_widget.setStyleSheet("background-color: grey;")
        top_layout = QHBoxLayout(navbar_widget)

        # Add buttons to the navbar
        self.button_1 = QPushButton("▶️")
        self.button_1.setFixedSize(40, 40)
        self.button_1.setStyleSheet("background-color: #FFB3BA; border: none; border-radius: 3px; padding: 5px; ")
        self.button_1.clicked.connect(self.run_code)
        top_layout.addWidget(self.button_1)

        button_colors = [
            "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#B4A7D6",
            "#D5A6BD", "#A9D18E", "#D5E8D4", "#E1D5E7", "#FFF2CC"
        ]

        for color in button_colors:
            button = QPushButton()
            button.setFixedSize(40, 40)
            button.setStyleSheet(f"background-color: {color}; border: none; border-radius: 10px;")
            top_layout.addWidget(button)

        search_bar_nav = QLineEdit()
        search_bar_nav.setPlaceholderText("Search")
        search_bar_nav.setFixedHeight(40)
        search_bar_nav.setStyleSheet("background-color: white; border-radius: 10px; padding: 5px;")
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
        sidebar_widget.setStyleSheet("background-color: #F0F0F0; border-radius: 10px;")

        self.sidebar_buttons = {}
        sidebar_items = [
            "Project View",
            "UI Code Editor",
            "JS Editor",
            "Business Func Editor",
            "JSON Editor",
            "BVO Editor"
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

    def update_selected_button(self, button_name):
        if self.current_button:
            self.current_button.setStyleSheet("""
                font-size: 16px;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #E0E0E0;
            """)
        
        self.current_button = self.sidebar_buttons[button_name]
        self.current_button.setStyleSheet("""
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
            
        if "RDF_JS_OBJ" in file_path:
            if not self.js_editor_instance:
                self.js_editor_instance = JsEditor()
            self.load_js_lib_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.js_editor_instance.set_code(code)
            self.update_selected_button("JS Editor")
            
        if "RDF_BF" in file_path:
            if not self.biz_func_editor_instance:
                self.biz_func_editor_instance = PhpEditorBF()
            self.load_biz_func_editor()
            with open(file_path, 'r') as file:
                code = file.read()
            self.biz_func_editor_instance.set_code(code)
            self.update_selected_button("Business Func Editor")
        
        if "RDF_JSON" in file_path:
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
