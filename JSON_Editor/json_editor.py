from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import json

class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # JSON key format
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#38ffa1"))
        key_format.setFontWeight(QFont.Weight.Bold)
        key_pattern = QRegularExpression(r'".*?":\s*')
        self.highlighting_rules.append((key_pattern, key_format))

        # JSON value format
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#329fe1"))
        value_pattern = QRegularExpression(r':\s*".*?"')
        self.highlighting_rules.append((value_pattern, value_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class JsonEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #1b1e28; border-radius: 10px;")

        # Create content layout for JSON Editor
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        content_widget.setStyleSheet("background-color: #232228; border-radius: 10px;")

        # Add search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Hi, Tell me what JSON you want to make!")
        search_bar.setFixedHeight(40)
        search_bar.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        content_layout.addWidget(search_bar)

        # Add JSON editor
        self.json_editor = QTextEdit()
        self.json_editor.setPlaceholderText("JSON Editor")
        self.json_editor.setStyleSheet("background-color: #323234; color: #FFFFFF; padding: 10px;")

        # Set the font for the text editor
        font = QFont("Consolas", 12)
        self.json_editor.setFont(font)

        content_layout.addWidget(self.json_editor)

        # Add syntax highlighter
        self.highlighter = JsonHighlighter(self.json_editor.document())

        # Connect text changed signal to update mobile view
        self.json_editor.textChanged.connect(self.update_mobile_view)

        # Right layout for mobile view
        mobile_view_layout = QVBoxLayout()
        mobile_view_widget = QWidget()
        mobile_view_widget.setLayout(mobile_view_layout)
        mobile_view_widget.setFixedWidth(400)  # Adjusted width
        mobile_view_widget.setFixedHeight(680)  # Adjusted height
        mobile_view_layout.setContentsMargins(0, 25, 0, 25)
        mobile_view_widget.setStyleSheet("background-color: #232228; border-radius: 10px; padding:20px;border-width: 10px; ")

        self.mobile_view = QWebEngineView()
        self.mobile_view.setStyleSheet("background-color: #FFFFFF; border-radius: 20px; padding:20px;")
        mobile_view_layout.addWidget(self.mobile_view)  # Adjusted size

        # Combine content area and mobile view
        main_content_layout = QHBoxLayout()
        main_content_layout.addWidget(content_widget)
        main_content_layout.addWidget(mobile_view_widget)

        self.setLayout(main_content_layout)

        # Call the update_mobile_view method to render the initial JSON code
        self.update_mobile_view()

    def update_mobile_view(self):
        json_code = self.json_editor.toPlainText()
        if json_code:
            try:
                parsed_json = json.loads(json_code)
                html_code = self.generate_tree_html(parsed_json)
                self.mobile_view.setHtml(html_code)
            except json.JSONDecodeError:
                self.mobile_view.setHtml("<p style='color: red;'>Invalid JSON</p>")
        else:
            self.mobile_view.setHtml("")

    def generate_tree_html(self, data, level=0):
        html = ""
        indent = "&nbsp;" * (level * 4)
        if isinstance(data, dict):
            html += f"{indent}<details>\n"
            html += f"{indent}&nbsp;&nbsp;<summary>&#x1F4C2; Object</summary>\n"
            html += f"{indent}&nbsp;&nbsp;<ul>\n"
            for key, value in data.items():
                html += f"{indent}&nbsp;&nbsp;&nbsp;&nbsp;<li>{key}: {self.generate_tree_html(value, level + 2)}</li>\n"
            html += f"{indent}&nbsp;&nbsp;</ul>\n"
            html += f"{indent}</details>\n"
        elif isinstance(data, list):
            html += f"{indent}<details>\n"
            html += f"{indent}&nbsp;&nbsp;<summary>&#x1F4C3; Array</summary>\n"
            html += f"{indent}&nbsp;&nbsp;<ul>\n"
            for item in data:
                html += f"{indent}&nbsp;&nbsp;&nbsp;&nbsp;<li>{self.generate_tree_html(item, level + 2)}</li>\n"
            html += f"{indent}&nbsp;&nbsp;</ul>\n"
            html += f"{indent}</details>\n"
        else:
            html += str(data)
        return html

    def set_code(self, code):
        self.json_editor.setPlainText(code)
        self.update_mobile_view()
