from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit, QPushButton, QScrollBar, QMessageBox, QApplication
from PyQt6.QtCore import Qt, QUrl, QRegularExpression
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Rule_Engine')))
from Rule_Engine.rule_engine import HtmlRuleEngine

class PhpHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        try:
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
        except Exception as e:
            print(f"Error initializing PhpHighlighter: {e}")

    def highlightBlock(self, text):
        try:
            for pattern, format in self.highlighting_rules:
                expression = QRegularExpression(pattern)
                iterator = expression.globalMatch(text)
                while iterator.hasNext():
                    match = iterator.next()
                    self.setFormat(match.capturedStart(), match.capturedLength(), format)
        except Exception as e:
            print(f"Error in highlightBlock: {e}")

class PhpEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        try:
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

            # Add collapsible terminal
            self.terminal = QTextEdit()
            self.terminal.setPlaceholderText("Terminal")
            self.terminal.setStyleSheet("background-color: #323234; color: #FFFFFF; padding: 10px;")
            self.terminal.setVisible(False)  # Hide terminal initially
            self.terminal.setVerticalScrollBar(QScrollBar())
            self.terminal.verticalScrollBar().setStyleSheet("background-color: #2e2e2e;")

            # Stylish buttons
            self.terminal_toggle_button_up = QPushButton("▲")
            self.terminal_toggle_button_up.setFixedWidth(30)
            self.terminal_toggle_button_up.setStyleSheet("""
                QPushButton {
                    color: #fcfcfc;
                    background-color: #323234;
                    border: none;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            """)
            self.terminal_toggle_button_up.clicked.connect(self.hide_terminal)

            self.terminal_toggle_button_down = QPushButton("▼")
            self.terminal_toggle_button_down.setFixedWidth(30)
            self.terminal_toggle_button_down.setStyleSheet("""
                QPushButton {
                    color: #fcfcfc;
                    background-color: #323234;
                    border: none;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            """)
            self.terminal_toggle_button_down.clicked.connect(self.show_terminal)
            self.terminal_toggle_button_down.setVisible(False)  # Hide initially

            terminal_toggle_layout = QHBoxLayout()
            terminal_toggle_layout.addWidget(self.terminal_toggle_button_up, alignment=Qt.AlignmentFlag.AlignLeft)
            terminal_toggle_layout.addWidget(self.terminal_toggle_button_down, alignment=Qt.AlignmentFlag.AlignLeft)

            content_layout.addLayout(terminal_toggle_layout)
            content_layout.addWidget(self.terminal)

            # Right layout for browser view
            mobile_view_layout = QVBoxLayout()
            mobile_view_widget = QWidget()
            mobile_view_widget.setLayout(mobile_view_layout)
            mobile_view_widget.setFixedWidth(400)  # Adjusted width
            mobile_view_widget.setFixedHeight(680)  # Adjusted height
            mobile_view_layout.setContentsMargins(0, 25, 0, 25)
            mobile_view_widget.setStyleSheet("background-color: #232228; border-radius: 10px; padding:20px;border-width: 10px; ")

            # URL input for browser view
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
            self.web_view.setFixedSize(360, 540)  # Adjusted size to fit with URL input

            mobile_view_layout.addWidget(self.web_view, 0, Qt.AlignmentFlag.AlignCenter)

            # Combine content area and browser view
            main_content_layout = QHBoxLayout()
            main_content_layout.addWidget(content_widget)
            main_content_layout.addWidget(mobile_view_widget)

            self.setLayout(main_content_layout)

            # Call the update_mobile_view method to render the initial HTML
            self.update_mobile_view()

            # Connect the textChanged signal to the update_mobile_view slot
            self.php_editor.textChanged.connect(self.update_mobile_view)
        except Exception as e:
            self.show_error_message(f"Error initializing PhpEditor: {e}")

    def hide_terminal(self):
        try:
            self.terminal.hide()
            self.terminal_toggle_button_up.setVisible(False)
            self.terminal_toggle_button_down.setVisible(True)
        except Exception as e:
            self.show_error_message(f"Error hiding terminal: {e}")

    def show_terminal(self):
        try:
            self.terminal.show()
            self.terminal.setFixedHeight(self.php_editor.height() // 3)  # Set the height of the terminal to one-third of the php_editor
            self.terminal_toggle_button_up.setVisible(True)
            self.terminal_toggle_button_down.setVisible(False)
        except Exception as e:
            self.show_error_message(f"Error showing terminal: {e}")

    def update_mobile_view(self):
        try:
            html_code = self.php_editor.toPlainText()
            css_code = """
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                }
                .container {
                    width: 100%;
                    height: 100%;
                    overflow: auto;
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start;
                    align-items: center;
                    box-sizing: border-box;
                    padding: 20px;
                }
            </style>
            """
            self.web_view.setHtml(css_code + '<div class="container">' + html_code + '</div>')
        except Exception as e:
            self.show_error_message(f"Error updating mobile view: {e}")

    def set_code(self, code):
        try:
            self.php_editor.setPlainText(code)
            self.update_mobile_view()
        except Exception as e:
            self.show_error_message(f"Error setting code: {e}")

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
                self.terminal.setPlainText("\n".join(errors))
                self.show_terminal()
            else:
                self.terminal.setPlainText("No errors found!")
                self.hide_terminal()
        except Exception as e:
            self.terminal.setPlainText(f"An error occurred during validation: {str(e)}")
            self.show_terminal()

    def load_url(self):
        try:
            url = self.url_input.text()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            self.web_view.setUrl(QUrl(url))
        except Exception as e:
            self.show_error_message(f"Failed to load URL: {e}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        editor = PhpEditor()
        editor.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Application failed to start: {e}")
