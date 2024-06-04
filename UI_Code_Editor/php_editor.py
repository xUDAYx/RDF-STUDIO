from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QApplication
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys

class PhpEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        # Create content layout for PHP Editor
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

        # Add PHP editor
        self.php_editor = QTextEdit()
        self.php_editor.setPlaceholderText("PHP Editor")
        self.php_editor.setStyleSheet("background-color: #A9A9A9; color: #FFFFFF;")
        content_layout.addWidget(self.php_editor)

        # Right layout for mobile view
        mobile_view_layout = QVBoxLayout()
        mobile_view_widget = QWidget()
        mobile_view_widget.setLayout(mobile_view_layout)
        mobile_view_widget.setFixedWidth(300)  # Adjusted width
        mobile_view_widget.setFixedHeight(600)  # Adjusted height
        mobile_view_widget.setStyleSheet("background-color: #000000; border-radius: 10px; border:3px solid black; padding: 20px;")

        # URL input for mobile view
        url_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setFixedHeight(40)
        self.url_input.setStyleSheet("background-color:white;border-radius: 10px;border:2px solid black; padding: 5px;")
        url_layout.addWidget(self.url_input)

        load_button = QPushButton("Load")
        load_button.setFixedHeight(40)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #45a049;
            }
        """)
        load_button.clicked.connect(self.load_url)
        url_layout.addWidget(load_button)

        mobile_view_layout.addLayout(url_layout)

        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background-color: #FFFFFF; border-radius: 20px;")
        self.web_view.setFixedSize(260, 500)  # Adjusted size to fit with URL input

        mobile_view_layout.addWidget(self.web_view, 0, Qt.AlignmentFlag.AlignCenter)

        # Combine content area and mobile view
        main_content_layout = QHBoxLayout()
        main_content_layout.addWidget(content_widget)
        main_content_layout.addWidget(mobile_view_widget)

        self.setLayout(main_content_layout)

    def run_php(self):
        php_code = self.php_editor.toPlainText()
        # Here, you would execute the PHP code (e.g., send it to a server for execution)
        # For simplicity, let's assume we just want to display the PHP code
        self.web_view.setHtml("<pre>" + php_code + "</pre>")

    def set_code(self, code):
        self.php_editor.setPlainText(code)

    def load_url(self):
        url = self.url_input.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        try:
            self.web_view.setUrl(QUrl(url))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load URL: {e}")


