from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

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
        # run_button = QPushButton("Run PHP")
        # run_button.setFixedHeight(40)
        # run_button.setStyleSheet("""
        #     background-color: #4CAF50; 
        #     color: white; 
        #     border: none; 
        #     border-radius: 10px;
        # """)
        # run_button.clicked.connect(self.run_php)
        # content_layout.addWidget(run_button)

    def run_php(self):
        php_code = self.php_editor.toPlainText()
        # Here, you would execute the PHP code (e.g., send it to a server for execution)
        # For simplicity, let's assume we just want to display the PHP code
        self.web_view.setHtml("<pre>" + php_code + "</pre>")

    def set_code(self, code):
        self.php_editor.setPlainText(code)
