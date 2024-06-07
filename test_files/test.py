import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QStackedWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RDF Studio | Python | Generative AI")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_widget.setStyleSheet("background-color: #E6E6FA;")  # Light purple background

        # Top layout for colored buttons and search bar
        top_layout = QHBoxLayout()

        # Add 11 colored buttons to the left side of the navbar
        button_1 = QPushButton("▶️")
        button_1.setFixedSize(40, 40)
        button_1.setStyleSheet("background-color: #FFB3BA; border: none; border-radius: 10px; padding: 5px; ")
        button_1.clicked.connect(self.run_html)
        top_layout.addWidget(button_1)

        for i in range(2, 12):
            button = QPushButton()
            button.setFixedSize(40, 40)
            button.setStyleSheet(f"background-color: #{hex(0xFFF300 + i * 10000)[2:]}; border: none; border-radius: 10px;")
            top_layout.addWidget(button)

        search_bar_nav = QLineEdit()
        search_bar_nav.setPlaceholderText("Search")
        search_bar_nav.setFixedHeight(40)
        search_bar_nav.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        top_layout.addWidget(search_bar_nav)

        top_layout.setSpacing(10)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # Set the top layout background color to grey
        top_layout_widget = QWidget()
        top_layout_widget.setLayout(top_layout)
        top_layout_widget.setStyleSheet("background-color: #D3D3D3; ")

        main_layout.addWidget(top_layout_widget)

        # Left layout for sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet("background-color: #F0F0F0; border-radius: 10px;")

        sidebar_items = [
            "Project View",
            "UI Designer",
            "UI Code Editor",
            "JS Lib Editor",
            "Web part Editor",
            "Biz Function Editor",
            "Com' Func' Editor",
            "BVO Editor",
            "JSON Editor"
        ]

        self.stack = QStackedWidget()
        self.editor_widgets = {}

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
            button.clicked.connect(lambda checked, item=item: self.display_editor(item))
            sidebar_layout.addWidget(button)

            editor = QTextEdit()
            editor.setStyleSheet("background-color: #FFFFFF;")
            self.editor_widgets[item] = editor
            self.stack.addWidget(editor)

        sidebar_layout.addStretch(1)

        # Central layout for main content area
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Hi, Tell me what UI you want to make!")
        search_bar.setFixedHeight(40)
        search_bar.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        content_layout.addWidget(search_bar)

        # Add HTML
        # Add HTML editor
        self.html_editor = QTextEdit()
        self.html_editor.setPlaceholderText("HTML Editor")
        self.html_editor.setStyleSheet("background-color: #A9A9A9; color: #FFFFFF;")
        content_layout.addWidget(self.html_editor)

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

        # Combine sidebar, content area, and mobile view
        main_content_layout = QHBoxLayout()
        main_content_layout.addWidget(sidebar_widget)
        main_content_layout.addWidget(content_widget)
        main_content_layout.addWidget(mobile_view_widget)

        main_layout.addLayout(main_content_layout)

        self.setCentralWidget(main_widget)

    def display_editor(self, item):
        self.stack.setCurrentWidget(self.editor_widgets[item])

    def run_html(self):
        html_code = self.html_editor.toPlainText()
        self.web_view.setHtml(html_code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
