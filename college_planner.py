import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QCalendarWidget, QListWidget, QListWidgetItem,
                            QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor

class TaskItem(QListWidgetItem):
    def __init__(self, title, deadline, priority):
        super().__init__()
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.setText(f"{title} - Due: {deadline} [{priority}]")

class CollegePlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart College Planner")
        self.setMinimumSize(1200, 800)
        self.is_dark_mode = False
        self.setup_database()
        self.setup_ui()
        self.load_tasks()
        
    def setup_database(self):
        self.conn = sqlite3.connect('college_planner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             deadline TEXT NOT NULL,
             priority TEXT NOT NULL)
        ''')
        self.conn.commit()

    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left panel (Calendar and Task Input)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Theme toggle button
        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # Task input section
        task_input = QWidget()
        task_layout = QVBoxLayout(task_input)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task Title")
        self.title_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)
        
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        add_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        task_layout.addWidget(QLabel("New Task"))
        task_layout.addWidget(self.title_input)
        task_layout.addWidget(QLabel("Priority"))
        task_layout.addWidget(self.priority_combo)
        task_layout.addWidget(add_button)
        
        # Add widgets to left panel
        left_layout.addWidget(self.theme_button)
        left_layout.addWidget(self.calendar)
        left_layout.addWidget(task_input)
        
        # Right panel (Task List)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        self.task_list = QListWidget()
        self.task_list.setDragEnabled(True)
        self.task_list.setAcceptDrops(True)
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        
        right_layout.addWidget(QLabel("Tasks"))
        right_layout.addWidget(self.task_list)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        # Apply initial theme
        self.apply_theme()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_button.setText("☀️" if self.is_dark_mode else "🌙")
        self.apply_theme()
        
    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                    color: white;
                }
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
                }
                QCalendarWidget {
                    background-color: #2d2d2d;
                    color: white;
                }
                QLineEdit, QComboBox {
                    background-color: #2d2d2d;
                    color: white;
                    border-color: #3d3d3d;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: white;
                }
                QListWidget::item {
                    border-color: #3d3d3d;
                }
                QListWidget::item:selected {
                    background-color: #3d3d3d;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                    color: black;
                }
                QWidget {
                    background-color: #f5f5f5;
                    color: black;
                }
                QCalendarWidget {
                    background-color: white;
                    color: black;
                }
                QLineEdit, QComboBox {
                    background-color: white;
                    color: black;
                    border-color: #ddd;
                }
                QListWidget {
                    background-color: white;
                    color: black;
                }
                QListWidget::item {
                    border-color: #ddd;
                }
                QListWidget::item:selected {
                    background-color: #e3f2fd;
                }
            """)

    def add_task(self):
        title = self.title_input.text()
        if not title:
            QMessageBox.warning(self, "Warning", "Please enter a task title!")
            return
            
        deadline = self.calendar.selectedDate().toString("yyyy-MM-dd")
        priority = self.priority_combo.currentText()
        
        # Add to database
        self.cursor.execute('''
            INSERT INTO tasks (title, deadline, priority)
            VALUES (?, ?, ?)
        ''', (title, deadline, priority))
        self.conn.commit()
        
        # Add to UI
        task_item = TaskItem(title, deadline, priority)
        self.task_list.addItem(task_item)
        
        # Clear input
        self.title_input.clear()
        
        # Animate new item
        self.animate_new_item(task_item)

    def animate_new_item(self, item):
        animation = QPropertyAnimation(item, b"opacity")
        animation.setDuration(500)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()

    def load_tasks(self):
        self.cursor.execute('SELECT title, deadline, priority FROM tasks')
        for title, deadline, priority in self.cursor.fetchall():
            task_item = TaskItem(title, deadline, priority)
            self.task_list.addItem(task_item)

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    planner = CollegePlanner()
    planner.show()
    sys.exit(app.exec()) 