from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLineEdit, QTreeView
from PyQt6.QtCore import Qt, QRegularExpression 
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont,QStandardItemModel, QStandardItem
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

        self.setStyleSheet("background-color: #232228; border-radius: 10px;")

        # Create content layout for JSON Editor
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        content_widget.setStyleSheet("background-color: #232228; border-radius: 10px;")
        
        # Add search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search your JSON data...")
        search_bar.setFixedHeight(40)
        search_bar.setStyleSheet("background-color:white;border-radius: 10px; padding: 5px;")
        content_layout.addWidget(search_bar)

        # Add JSON editor
        self.json_editor = QTextEdit()
        self.json_editor.setPlaceholderText("JSON Editor")
        self.json_editor.setStyleSheet("background-color: #323234; color: #FFFFFF; padding: 10px;")
        content_layout.addWidget(self.json_editor)

        # Right layout for mobile view
        mobile_view_layout = QVBoxLayout()
        mobile_view_widget = QWidget()
        mobile_view_widget.setLayout(mobile_view_layout)
        mobile_view_widget.setFixedWidth(400)  # Adjusted width
        mobile_view_widget.setFixedHeight(680)  # Adjusted height
        mobile_view_layout.setContentsMargins(0, 25, 0, 25)
        mobile_view_widget.setStyleSheet("background-color: #232228; border-radius: 10px; padding:20px;border-width: 10px; ")

        self.tree_view = QTreeView()
        self.tree_view.setStyleSheet("color: black; background-color: white; border: none;")
        mobile_view_layout.addWidget(self.tree_view)

        # Combine content area and mobile view
        main_content_layout = QHBoxLayout()
        main_content_layout.addWidget(content_widget)
        main_content_layout.addWidget(mobile_view_widget)

        self.setLayout(main_content_layout)

        # Connect text changed signal to update tree view
        self.json_editor.textChanged.connect(self.update_tree_view)

    def update_tree_view(self):
        json_code = self.json_editor.toPlainText()
        if json_code:
                parsed_json = json.loads(json_code)
                self.populate_tree_view(parsed_json)

    def populate_tree_view(self, data):
        model = QStandardItemModel()
        self.tree_view.setModel(model)
        self.add_json_to_model(data, model.invisibleRootItem())

    def add_json_to_model(self, data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                key_item = QStandardItem(str(key))
                value_item = QStandardItem(str(value))
                parent.appendRow([key_item, value_item])
                if isinstance(value, (dict, list)):
                    self.add_json_to_model(value, key_item)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                key_item = QStandardItem(str(index))
                value_item = QStandardItem(str(value))
                parent.appendRow([key_item, value_item])
                if isinstance(value, (dict, list)):
                    self.add_json_to_model(value, key_item)
    
    def set_code(self, json_code):
        self.json_editor.setPlainText(json_code)
