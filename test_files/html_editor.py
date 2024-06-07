# html_editor.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

class HtmlEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('HTML Code Editor with Live Preview')
        self.setGeometry(100, 100, 1000, 600)

        # Layouts
        main_layout = QVBoxLayout()
        editor_layout = QVBoxLayout()
        preview_layout = QVBoxLayout()

        # HTML Editor
        self.html_editor = QTextEdit()
        self.html_editor.setPlaceholderText("Write your HTML code here...")
        editor_layout.addWidget(self.html_editor)

        # Run Button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_html)
        editor_layout.addWidget(self.run_button)

        # HTML Preview
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(375, 667)  # Size of an iPhone 8 for example
        preview_layout.addWidget(self.web_view)

        # Combine editor and preview
        editor_label = QLabel("HTML Editor")
        preview_label = QLabel("Mobile View Preview (iPhone 8 Size)")
        editor_layout.addWidget(editor_label)
        preview_layout.addWidget(preview_label)

        # Horizontal layout to place editor and preview side by side
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(editor_layout)
        horizontal_layout.addLayout(preview_layout)

        # Add horizontal layout to main layout
        main_layout.addLayout(horizontal_layout)
        self.setLayout(main_layout)

    def run_html(self):
        html_code = self.html_editor.toPlainText()
        self.web_view.setHtml(html_code)


def main():
    app = QApplication(sys.argv)
    editor = HtmlEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
