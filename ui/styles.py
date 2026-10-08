"""
Estilos para SHIFTMODE
"""

LIGHT_STYLESHEET = """
QMainWindow {
    background: #F6F7FB;
    color: #121212;
}

QWidget {
    background: #F6F7FB;
    color: #121212;
}

QTabWidget::pane {
    border: 1px solid #E7EAF0;
    background: #FFFFFF;
    border-radius: 12px;
}

QTabBar::tab {
    background: #F3F5F8;
    color: #20242A;
    border: 1px solid #E7EAF0;
    border-bottom: none;
    padding: 10px 18px;
    border-radius: 10px 10px 0 0;
    margin-right: 6px;
}

QTabBar::tab:selected {
    background: #0066FF;
    color: #FFFFFF;
}

QPushButton {
    background: #0066FF;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}

QPushButton:hover { background: #0055DD; }
QPushButton#dangerButton { background: #FF6B57; }
QPushButton#dangerButton:hover { background: #EC5D49; }
QPushButton#successButton { background: #2EB67D; }
QPushButton#successButton:hover { background: #24976A; }
QPushButton#ghostButton {
    background: #F3F5F8;
    color: #121212;
    border: 1px solid #E7EAF0;
}
QPushButton#ghostButton:hover { background: #E8ECF3; }

QFrame#card {
    background: #FFFFFF;
    border: 1px solid #E7EAF0;
    border-radius: 14px;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: 700;
    color: #121212;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #7A7F8A;
}

QLabel#metricValue {
    font-size: 22px;
    font-weight: 700;
    color: #121212;
}

QLabel#metricLabel {
    font-size: 11px;
    color: #7A7F8A;
}

QLabel#profileName {
    font-size: 20px;
    font-weight: 700;
}

QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox {
    background: #F3F5F8;
    border: 1px solid #E7EAF0;
    border-radius: 10px;
    padding: 9px 10px;
    color: #121212;
}

QTableWidget {
    background: #FFFFFF;
    border: 1px solid #E7EAF0;
    border-radius: 10px;
    gridline-color: #EDF0F5;
}

QHeaderView::section {
    background: #F3F5F8;
    color: #121212;
    padding: 8px;
    border: none;
    font-weight: 600;
}

QScrollBar:vertical {
    background: #F3F5F8;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #D6D9E0;
    border-radius: 5px;
}
"""

DARK_STYLESHEET = """
QMainWindow {
    background: #121212;
    color: #F3F5F8;
}

QWidget {
    background: #121212;
    color: #F3F5F8;
}

QTabWidget::pane {
    border: 1px solid #2D2D2D;
    background: #1A1A1A;
    border-radius: 12px;
}

QTabBar::tab {
    background: #1F1F1F;
    color: #E8EAED;
    border: 1px solid #2D2D2D;
    border-bottom: none;
    padding: 10px 18px;
    border-radius: 10px 10px 0 0;
    margin-right: 6px;
}

QTabBar::tab:selected {
    background: #4DA3FF;
    color: #FFFFFF;
}

QPushButton {
    background: #4DA3FF;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}

QPushButton:hover { background: #2D8CF5; }
QPushButton#dangerButton { background: #FF7A5C; }
QPushButton#dangerButton:hover { background: #E96B4E; }
QPushButton#successButton { background: #2EB67D; }
QPushButton#successButton:hover { background: #24976A; }
QPushButton#ghostButton {
    background: #1F1F1F;
    color: #F3F5F8;
    border: 1px solid #2D2D2D;
}
QPushButton#ghostButton:hover { background: #2B2B2B; }

QFrame#card {
    background: #1A1A1A;
    border: 1px solid #2D2D2D;
    border-radius: 14px;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: 700;
    color: #F3F5F8;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #A2A7B3;
}

QLabel#metricValue {
    font-size: 22px;
    font-weight: 700;
    color: #F3F5F8;
}

QLabel#metricLabel {
    font-size: 11px;
    color: #A2A7B3;
}

QLabel#profileName {
    font-size: 20px;
    font-weight: 700;
}

QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox {
    background: #1F1F1F;
    border: 1px solid #2D2D2D;
    border-radius: 10px;
    padding: 9px 10px;
    color: #F3F5F8;
}

QTableWidget {
    background: #1A1A1A;
    border: 1px solid #2D2D2D;
    border-radius: 10px;
    gridline-color: #2D2D2D;
}

QHeaderView::section {
    background: #1F1F1F;
    color: #F3F5F8;
    padding: 8px;
    border: none;
    font-weight: 600;
}

QScrollBar:vertical {
    background: #1F1F1F;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #3A3A3A;
    border-radius: 5px;
}
"""
