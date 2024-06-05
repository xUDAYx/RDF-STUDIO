from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

class HTMLEditor(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        # HTML editor
        self.html_editor = QTextEdit()
        self.html_editor.setPlaceholderText("HTML Editor")
        self.html_editor.setStyleSheet("background-color: #A9A9A9; color: #FFFFFF;")
        layout.addWidget(self.html_editor)

        # Mobile view
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

        layout.addWidget(mobile_view_widget)

    def get_html_code(self):
        return self.html_editor.toPlainText()
