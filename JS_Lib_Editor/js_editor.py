from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt

class JsEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        # Create content layout for JS Editor
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        content_widget.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        # Add search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Hi, Tell me what UI you want to make!")
        search_bar.setFixedHeight(40)
        search_bar.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        content_layout.addWidget(search_bar)

        # Add JS editor
        self.js_editor = QTextEdit()
        self.js_editor.setPlaceholderText("JS Editor")
        self.js_editor.setStyleSheet("background-color: #A9A9A9; color: #FFFFFF;")
        content_layout.addWidget(self.js_editor)

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

    def set_code(self, code):
        self.js_editor.setText(code)

    def run_js(self):
        js_code = self.js_editor.toPlainText()
        # Here, you would execute the JS code (e.g., send it to a server for execution)
        # For simplicity, let's assume we just want to display the JS code
        self.web_view.setHtml("<pre>" + js_code + "</pre>")
