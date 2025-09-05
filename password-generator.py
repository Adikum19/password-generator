import sys
import random
import string
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QCheckBox, QSlider, QHBoxLayout, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard


def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return ""

    return ''.join(random.choice(characters) for _ in range(length))

def calculate_password_strength(password):
    score = 0
    feedback = []
    
    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    
    
    if score <= 2:
        strength = "Weak"
        color = "red"
    elif score <= 4:
        strength = "Medium"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"
    
    return strength, color, score

# PyQt6 
class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Password Generator")
        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(450, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.developer_label = QLabel("Developed By. ahmetcakir-dev")
        self.developer_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.developer_label.setStyleSheet("""
            font-size: 12px;
            color: red;
            font-style: Bold;
            font-family: Book Antiqua;
            margin-bottom: 12px;
        """)
        layout.addWidget(self.developer_label)

        self.strength_label = QLabel("Password Strength: Not calculated yet")
        self.strength_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        """)
        layout.addWidget(self.strength_label)

        self.strength_progress = QProgressBar()
        self.strength_progress.setRange(0, 6)
        self.strength_progress.setValue(0)
        self.strength_progress.setTextVisible(False)
        self.strength_progress.setFixedHeight(20)
        self.strength_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 10px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.strength_progress)

        self.password_label = QLabel("Generated Password:")
        self.password_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2E3440;
            padding: 10px;
            background-color: #ECEFF4;
            border-radius: 8px;
            margin: 10px 0;
        """)
        layout.addWidget(self.password_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.generate_button = QPushButton("🔐 Generate Password")
        self.generate_button.clicked.connect(self.on_generate)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #4C566A;
            }
        """)
        button_layout.addWidget(self.generate_button)

        self.copy_button = QPushButton("📋 Copy Password")
        self.copy_button.clicked.connect(self.on_copy)
        self.copy_button.setEnabled(False)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #A3BE8C;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #B48EAD;
            }
            QPushButton:pressed {
                background-color: #8FBCBB;
            }
            QPushButton:disabled {
                background-color: #D8DEE9;
                color: #888;
            }
        """)
        button_layout.addWidget(self.copy_button)

        layout.addLayout(button_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        self.setLayout(layout)

    def on_generate(self):
        self.current_password = generate_password()
        self.password_label.setText(f"Generated Password: {self.current_password}")
        strength, color, score = calculate_password_strength(self.current_password)
        self.strength_label.setText(f"Password Strength: {strength} ({score}/6)")
        self.strength_label.setStyleSheet(f"color: {color}; font-weight: bold;")

        self.strength_progress.setValue(score)
        if score <= 2:
            self.strength_progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        elif score <= 4:
            self.strength_progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
        else:
            self.strength_progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")

        self.copy_button.setEnabled(True)

    def on_copy(self):
        if hasattr(self, 'current_password'):
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_password)
            self.copy_button.setText("Copied!")
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: self.copy_button.setText("Copy Password"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
