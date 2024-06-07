from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit,QMessageBox,QPushButton
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Rule_Engine')))
from Rule_Engine.rule_engine import HtmlRuleEngine 

class PhpHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # HTML tag format
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#38ffa1"))
        tag_format.setFontWeight(QFont.Weight.Bold)
        tag_pattern = QRegularExpression(r"</?[\w\s]*>")
        self.highlighting_rules.append((tag_pattern, tag_format))

        # HTML attribute format
        attribute_format = QTextCharFormat()
        attribute_format.setForeground(QColor("#f5dec1"))
        attribute_pattern = QRegularExpression(r'\b\w+="')
        self.highlighting_rules.append((attribute_pattern, attribute_format))

        # HTML value format
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#329fe1"))
        value_pattern = QRegularExpression(r'".*?"')
        self.highlighting_rules.append((value_pattern, value_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class PhpEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #1b1e28; border-radius: 10px;")

        # Create content layout for PHP Editor
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        content_widget.setStyleSheet("background-color: #232228; border-radius: 10px;")

        # Add search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Hi, Tell me what UI you want to make!")
        search_bar.setFixedHeight(40)
        search_bar.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        content_layout.addWidget(search_bar)

        # Add PHP editor
        self.php_editor = QTextEdit()
        self.php_editor.setPlaceholderText("PHP Editor")
        self.php_editor.setStyleSheet("background-color: #323234; color: #FFFFFF; padding: 10px;")

        # Set the font for the text editor
        font = QFont("Consolas", 12)
        self.php_editor.setFont(font)

        content_layout.addWidget(self.php_editor)

        # Add syntax highlighter
        self.highlighter = PhpHighlighter(self.php_editor.document())

        validate_button = QPushButton("Validate HTML")
        validate_button.setStyleSheet("color: #fcfcfc;")
        validate_button.clicked.connect(self.validate_html)
        content_layout.addWidget(validate_button)

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

        # Call the update_mobile_view method to render the initial HTML
        self.update_mobile_view()

        # Connect the textChanged signal to the update_mobile_view slot
        self.php_editor.textChanged.connect(self.update_mobile_view)

    def update_mobile_view(self):
        html_code = self.php_editor.toPlainText()
        css_code = """
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
             
            }
        </style>
        """
        self.mobile_view.setHtml(css_code + html_code)

    def set_code(self, code):
        self.php_editor.setPlainText(code)
        self.update_mobile_view()
    def validate_html(self):
        try:
            html_code = self.php_editor.toPlainText()
            rules_file_path = os.path.join(os.path.dirname(__file__), '..', 'Rule_Engine', 'rules.json')
            rules_file_path = os.path.abspath(rules_file_path)  # Get absolute path
            print(f"Using rules file path: {rules_file_path}")  # Debugging information

            if not os.path.exists(rules_file_path):
                raise FileNotFoundError(f"rules.json not found at {rules_file_path}")

            rule_engine = HtmlRuleEngine(rules_file_path)
            errors = rule_engine.apply_rules(html_code)
            if errors:
                QMessageBox.warning(self, "Validation Errors", "\n".join(errors))
            else:
                QMessageBox.information(self, "Validation", "No errors found!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during validation: {str(e)}")
