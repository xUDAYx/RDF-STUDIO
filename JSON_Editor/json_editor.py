from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
import json

class JsonEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        # Create content layout for JSON Editor
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        content_widget.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
        
        # Add search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search your JSON data...")
        search_bar.setFixedHeight(40)
        search_bar.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        content_layout.addWidget(search_bar)

        # Add JSON editor
        self.json_editor = QTextEdit()
        self.json_editor.setPlaceholderText("JSON Editor")
        self.json_editor.setStyleSheet("background-color: #A9A9A9; color: #FFFFFF;")
        content_layout.addWidget(self.json_editor)

        # Right layout for mobile view
        mobile_view_layout = QVBoxLayout()
        mobile_view_widget = QWidget()
        mobile_view_widget.setLayout(mobile_view_layout)
        mobile_view_widget.setFixedWidth(300)  # Adjusted width
        mobile_view_widget.setFixedHeight(600)  # Adjusted height
        mobile_view_widget.setStyleSheet("background-color: #000000; border-radius: 30px; padding: 20px;")

        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background-color: #FFFFFF; border-radius: 20px;")
        self.web_view.setFixedSize(260, 580)  # Adjusted size

        mobile_view_layout.addWidget(self.web_view, 0, Qt.AlignmentFlag.AlignCenter)

        # Combine content area and mobile view
        main_content_layout = QHBoxLayout()
        main_content_layout.addWidget(content_widget)
        main_content_layout.addWidget(mobile_view_widget)

        self.setLayout(main_content_layout)

        # Add run button
        # run_button = QPushButton("Run JSON")
        # run_button.setFixedHeight(40)
        # run_button.setStyleSheet("""
        #     background-color: #4CAF50; 
        #     color: white; 
        #     border: none; 
        #     border-radius: 10px;
        # """)
        # run_button.clicked.connect(self.run_json)
        # content_layout.addWidget(run_button)

    def run_json(self):
        json_code = self.json_editor.toPlainText()
        try:
            parsed_json = json.loads(json_code)
            formatted_json = json.dumps(parsed_json, indent=4)
            self.web_view.setHtml(f"<pre>{formatted_json}</pre>")
            QMessageBox.information(self, "Success", "Valid JSON")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON:\n{str(e)}")

    def set_code(self, code):
        self.json_editor.setPlainText(code)
