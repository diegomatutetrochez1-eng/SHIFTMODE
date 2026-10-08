from __future__ import annotations

from datetime import datetime
from typing import Optional

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from config.database import init_db
from config.settings import APP_NAME, CHART_COLORS, DEFAULT_THEME, WINDOW_HEIGHT, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_WIDTH
from services.data_service import DataService
from ui.styles import DARK_STYLESHEET, LIGHT_STYLESHEET


class EmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo empleado")
        self.resize(420, 280)
        self.setModal(True)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.position_input = QLineEdit()

        form.addRow("Nombre", self.name_input)
        form.addRow("Correo", self.email_input)
        form.addRow("Teléfono", self.phone_input)
        form.addRow("Dirección", self.address_input)
        form.addRow("Cargo", self.position_input)

        buttons = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_employee)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)

        buttons.addStretch()
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)

        layout.addLayout(form)
        layout.addLayout(buttons)

    def save_employee(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        position = self.position_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Validación", "Nombre y correo son obligatorios.")
            return

        service = DataService()
        try:
            service.create_employee(name, email, phone, address, position)
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo guardar al empleado:\n{exc}")
        finally:
            service.close()


class AbsenceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar falta")
        self.resize(420, 260)
        self.setModal(True)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.employee_combo = QComboBox()
        self.reason_input = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["sick", "vacation", "unjustified", "disability"])
        self.half_day_combo = QComboBox()
        self.half_day_combo.addItems(["None", "am", "pm"])
        self.salary_input = QLineEdit("0")

        form.addRow("Empleado", self.employee_combo)
        form.addRow("Motivo", self.reason_input)
        form.addRow("Tipo", self.type_combo)
        form.addRow("Medio día", self.half_day_combo)
        form.addRow("Descuento", self.salary_input)

        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_absence)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)

        layout.addLayout(form)
        layout.addLayout(buttons)

    def set_employees(self, employees):
        self.employee_combo.clear()
        for employee in employees:
            self.employee_combo.addItem(employee.name, employee.id)

    def save_absence(self):
        employee_id = self.employee_combo.currentData()
        reason = self.reason_input.text().strip()
        absence_type = self.type_combo.currentText()
        half_day = self.half_day_combo.currentText()
        salary_deduction = float(self.salary_input.text() or 0)

        if not employee_id or not reason:
            QMessageBox.warning(self, "Validación", "Empleado y motivo son obligatorios.")
            return

        if half_day == "None":
            half_day = None

        service = DataService()
        try:
            service.add_absence(employee_id, datetime.now(), reason, absence_type, half_day, salary_deduction)
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo registrar la falta:\n{exc}")
        finally:
            service.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.theme = DEFAULT_THEME
        self.service = DataService()
        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self._init_ui()
        self.apply_theme()
        self.load_employees()
        self.refresh_dashboard()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        header = QFrame()
        header.setObjectName("card")
        header_layout = QHBoxLayout(header)

        title = QLabel("SHIFTMODE")
        title.setObjectName("titleLabel")
        subtitle = QLabel("Control de turnos, empleados y productividad")
        subtitle.setObjectName("subtitleLabel")

        title_col = QVBoxLayout()
        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        actions = QHBoxLayout()
        self.theme_toggle = QPushButton("Dark Mode")
        self.theme_toggle.setObjectName("ghostButton")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        actions.addWidget(self.theme_toggle)

        header_layout.addLayout(title_col)
        header_layout.addStretch()
        header_layout.addLayout(actions)

        self.tabs = QtWidgets.QTabWidget()
        self.dashboard_tab = QWidget()
        self.employees_tab = QWidget()
        self.shifts_tab = QWidget()
        self.absences_tab = QWidget()

        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.employees_tab, "Empleados")
        self.tabs.addTab(self.shifts_tab, "Turnos")
        self.tabs.addTab(self.absences_tab, "Faltas")

        main_layout.addWidget(header)
        main_layout.addWidget(self.tabs)

        self._build_dashboard()
        self._build_employee_tab()
        self._build_shift_tab()
        self._build_absence_tab()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "dark":
            self.setStyleSheet(DARK_STYLESHEET)
            self.theme_toggle.setText("Light Mode")
        else:
            self.setStyleSheet(LIGHT_STYLESHEET)
            self.theme_toggle.setText("Dark Mode")

    def _build_dashboard(self):
        layout = QVBoxLayout(self.dashboard_tab)

        cards = QHBoxLayout()
        self.kpi_total_employees = self._metric_card("Empleados", "0")
        self.kpi_total_hours = self._metric_card("Horas totales", "0h")
        self.kpi_today_hours = self._metric_card("Horas hoy", "0h")
        self.kpi_absences = self._metric_card("Faltas", "0")

        for card in [self.kpi_total_employees, self.kpi_total_hours, self.kpi_today_hours, self.kpi_absences]:
            cards.addWidget(card)

        body = QHBoxLayout()
        left = QFrame()
        left.setObjectName("card")
        left_layout = QVBoxLayout(left)
        self.calendar = QCalendarWidget()
        left_layout.addWidget(self.calendar)

        right = QFrame()
        right.setObjectName("card")
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("Top empleados por horas"))
        self.chart_canvas = self._build_chart_canvas()
        right_layout.addWidget(self.chart_canvas)

        body.addWidget(left, 1)
        body.addWidget(right, 1)

        self.daily_table = QTableWidget(0, 2)
        self.daily_table.setHorizontalHeaderLabels(["Fecha", "Horas"])
        self.daily_table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(cards)
        layout.addLayout(body)
        layout.addWidget(self.daily_table)

    def _metric_card(self, label, value):
        frame = QFrame()
        frame.setObjectName("card")
        layout = QVBoxLayout(frame)
        value_label = QLabel(value)
        value_label.setObjectName("metricValue")
        label_label = QLabel(label)
        label_label.setObjectName("metricLabel")
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        return frame

    def _build_chart_canvas(self):
        fig = Figure()
        fig.patch.set_facecolor("none")
        canvas = FigureCanvas(fig)
        return canvas

    def _build_employee_tab(self):
        layout = QHBoxLayout(self.employees_tab)

        left = QFrame()
        left.setObjectName("card")
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("Empleados"))
        self.employee_table = QTableWidget(0, 3)
        self.employee_table.setHorizontalHeaderLabels(["Nombre", "Correo", "Cargo"])
        self.employee_table.itemSelectionChanged.connect(self.load_selected_employee)
        left_layout.addWidget(self.employee_table)

        add_btn = QPushButton("Agregar empleado")
        add_btn.clicked.connect(self.open_employee_dialog)
        left_layout.addWidget(add_btn)

        right = QFrame()
        right.setObjectName("card")
        right_layout = QVBoxLayout(right)
        self.profile_name = QLabel("Selecciona un empleado")
        self.profile_name.setObjectName("profileName")
        self.detail_labels = [
            QLabel("Correo: -"),
            QLabel("Dirección: -"),
            QLabel("Hora de entrada: -"),
            QLabel("Hora de salida: -"),
            QLabel("Hora de almuerzo: -"),
        ]

        for label in self.detail_labels:
            right_layout.addWidget(label)

        self.employee_shifts_table = QTableWidget(0, 5)
        self.employee_shifts_table.setHorizontalHeaderLabels(["Fecha", "Entrada", "Salida", "Almuerzo", "Horas"])
        right_layout.addWidget(self.employee_shifts_table)

        layout.addWidget(left, 2)
        layout.addWidget(right, 3)

    def _build_shift_tab(self):
        layout = QVBoxLayout(self.shifts_tab)
        top = QFrame(); top.setObjectName("card")
        top_layout = QVBoxLayout(top)

        self.shift_combo = QComboBox()
        self.shift_status = QLabel("Selecciona un empleado")
        buttons = QHBoxLayout()

        btn_start = QPushButton("Shift Start")
        btn_start.setObjectName("successButton")
        btn_start.clicked.connect(self.action_start_shift)

        btn_lunch_start = QPushButton("Lunch Start")
        btn_lunch_start.clicked.connect(self.action_lunch_start)

        btn_lunch_end = QPushButton("Lunch End")
        btn_lunch_end.clicked.connect(self.action_lunch_end)

        btn_end = QPushButton("Shift End")
        btn_end.setObjectName("dangerButton")
        btn_end.clicked.connect(self.action_end_shift)

        buttons.addWidget(btn_start)
        buttons.addWidget(btn_lunch_start)
        buttons.addWidget(btn_lunch_end)
        buttons.addWidget(btn_end)

        top_layout.addWidget(self.shift_combo)
        top_layout.addWidget(self.shift_status)
        top_layout.addLayout(buttons)

        self.shift_table = QTableWidget(0, 7)
        self.shift_table.setHorizontalHeaderLabels(["Empleado", "Fecha", "Entrada", "Salida", "Almuerzo", "Horas", "Estado"])

        layout.addWidget(top)
        layout.addWidget(self.shift_table)

    def _build_absence_tab(self):
        layout = QVBoxLayout(self.absences_tab)
        form = QFrame(); form.setObjectName("card")
        form_layout = QVBoxLayout(form)

        self.absence_employee_combo = QComboBox()
        self.absence_reason = QLineEdit()
        self.absence_type = QComboBox()
        self.absence_type.addItems(["sick", "vacation", "unjustified", "disability"])
        self.absence_half_day = QComboBox()
        self.absence_half_day.addItems(["None", "am", "pm"])
        self.absence_salary = QLineEdit("0")

        sub_form = QFormLayout()
        sub_form.addRow("Empleado", self.absence_employee_combo)
        sub_form.addRow("Motivo", self.absence_reason)
        sub_form.addRow("Tipo", self.absence_type)
        sub_form.addRow("Medio día", self.absence_half_day)
        sub_form.addRow("Descuento", self.absence_salary)
        form_layout.addLayout(sub_form)

        buttons = QHBoxLayout()
        save_absence = QPushButton("Guardar falta")
        save_absence.clicked.connect(self.add_absence)
        buttons.addStretch(); buttons.addWidget(save_absence)
        form_layout.addLayout(buttons)

        self.absence_table = QTableWidget(0, 6)
        self.absence_table.setHorizontalHeaderLabels(["Empleado", "Fecha", "Tipo", "Motivo", "Medio día", "Descuento"])

        layout.addWidget(form)
        layout.addWidget(self.absence_table)

    def load_employees(self):
        employees = self.service.get_employees()
        self.employee_combo_options = employees
        self.employee_table.setRowCount(len(employees))
        self.employee_table.setColumnCount(3)
        for i, employee in enumerate(employees):
            self.employee_table.setItem(i, 0, QTableWidgetItem(employee.name))
            self.employee_table.setItem(i, 1, QTableWidgetItem(employee.email))
            self.employee_table.setItem(i, 2, QTableWidgetItem(employee.position or ""))

        self.shift_combo.clear()
        for employee in employees:
            self.shift_combo.addItem(employee.name, employee.id)
            self.absence_employee_combo.addItem(employee.name, employee.id)

        self.employee_table.resizeColumnsToContents()
        self.refresh_dashboard()
        self.refresh_shifts_table()
        self.refresh_absences_table()

    def load_selected_employee(self):
        rows = self.employee_table.selectionModel().selectedRows()
        if not rows:
            return
        row = rows[0].row()
        employees = self.service.get_employees()
        if row >= len(employees):
            return
        employee = employees[row]
        self._populate_employee_profile(employee)

    def _populate_employee_profile(self, employee):
        self.profile_name.setText(employee.name)
        self.detail_labels[0].setText(f"Correo: {employee.email}")
        self.detail_labels[1].setText(f"Dirección: {employee.address or '-'}")

        shifts = self.service.get_shifts_for_employee(employee.id)
        latest = shifts[0] if shifts else None
        if latest:
            self.detail_labels[2].setText(f"Hora de entrada: {latest.shift_start.strftime('%H:%M') if latest.shift_start else '-'}")
            self.detail_labels[3].setText(f"Hora de salida: {latest.shift_end.strftime('%H:%M') if latest.shift_end else '-'}")
            lunch_time = "-"
            if latest.lunch_start and latest.lunch_end:
                lunch_time = f"{latest.lunch_start.strftime('%H:%M')} - {latest.lunch_end.strftime('%H:%M')}"
            self.detail_labels[4].setText(f"Hora de almuerzo: {lunch_time}")
        else:
            for label in self.detail_labels[2:]:
                label.setText("-")

        self.employee_shifts_table.setRowCount(len(shifts))
        for i, shift in enumerate(shifts):
            self.employee_shifts_table.setItem(i, 0, QTableWidgetItem(shift.shift_date.strftime('%Y-%m-%d')))
            self.employee_shifts_table.setItem(i, 1, QTableWidgetItem(shift.shift_start.strftime('%H:%M') if shift.shift_start else '-'))
            self.employee_shifts_table.setItem(i, 2, QTableWidgetItem(shift.shift_end.strftime('%H:%M') if shift.shift_end else '-'))
            if shift.lunch_start and shift.lunch_end:
                lunch_value = f"{shift.lunch_start.strftime('%H:%M')} - {shift.lunch_end.strftime('%H:%M')}"
            else:
                lunch_value = '-'
            self.employee_shifts_table.setItem(i, 3, QTableWidgetItem(lunch_value))
            self.employee_shifts_table.setItem(i, 4, QTableWidgetItem(f"{shift.hours_worked}h" if shift.hours_worked else '0h'))

    def open_employee_dialog(self):
        dialog = EmployeeDialog(self)
        if dialog.exec_():
            self.load_employees()

    def action_start_shift(self):
        employee_id = self.shift_combo.currentData()
        if employee_id is None:
            QMessageBox.warning(self, "Sin empleado", "Selecciona un empleado antes de iniciar turno.")
            return
        shift = self.service.start_shift(employee_id)
        self.shift_status.setText(f"Turno iniciado para {self.shift_combo.currentText()} - {shift.shift_start.strftime('%H:%M')}")
        self.refresh_shifts_table()
        self.load_employees()

    def action_lunch_start(self):
        employee_id = self.shift_combo.currentData()
        if employee_id is None:
            QMessageBox.warning(self, "Sin empleado", "Selecciona un empleado antes de iniciar almuerzo.")
            return
        shift = self.service.lunch_start(employee_id)
        if not shift:
            QMessageBox.warning(self, "Sin turno", "Primero inicia el turno del empleado.")
            return
        self.shift_status.setText(f"Almuerzo iniciado para {self.shift_combo.currentText()}")
        self.refresh_shifts_table()

    def action_lunch_end(self):
        employee_id = self.shift_combo.currentData()
        if employee_id is None:
            QMessageBox.warning(self, "Sin empleado", "Selecciona un empleado antes de cerrar almuerzo.")
            return
        shift = self.service.lunch_end(employee_id)
        if not shift:
            QMessageBox.warning(self, "Sin turno", "Primero inicia el turno del empleado.")
            return
        self.shift_status.setText(f"Almuerzo terminado para {self.shift_combo.currentText()}")
        self.refresh_shifts_table()

    def action_end_shift(self):
        employee_id = self.shift_combo.currentData()
        if employee_id is None:
            QMessageBox.warning(self, "Sin empleado", "Selecciona un empleado antes de cerrar turno.")
            return
        shift = self.service.end_shift(employee_id)
        if not shift:
            QMessageBox.warning(self, "Sin turno", "No hay turno en progreso para este empleado.")
            return
        self.shift_status.setText(f"Turno finalizado para {self.shift_combo.currentText()} - {shift.hours_worked}h")
        self.refresh_shifts_table()
        self.load_employees()

    def add_absence(self):
        employee_id = self.absence_employee_combo.currentData()
        reason = self.absence_reason.text().strip()
        if employee_id is None or not reason:
            QMessageBox.warning(self, "Falta", "Selecciona un empleado y escribe un motivo.")
            return
        absence_type = self.absence_type.currentText()
        half_day = self.absence_half_day.currentText()
        if half_day == "None":
            half_day = None
        salary_deduction = float(self.absence_salary.text() or 0)

        self.service.add_absence(employee_id, datetime.now(), reason, absence_type, half_day, salary_deduction)
        self.absence_reason.clear(); self.absence_salary.setText("0")
        self.refresh_absences_table(); self.refresh_dashboard()

    def refresh_shifts_table(self):
        shifts = self.service.get_last_n_shifts(limit=100)
        self.shift_table.setRowCount(len(shifts))
        for i, shift in enumerate(shifts):
            employee = self.service.get_employee(shift.employee_id)
            self.shift_table.setItem(i, 0, QTableWidgetItem(employee.name if employee else "-"))
            self.shift_table.setItem(i, 1, QTableWidgetItem(shift.shift_date.strftime('%Y-%m-%d')))
            self.shift_table.setItem(i, 2, QTableWidgetItem(shift.shift_start.strftime('%H:%M') if shift.shift_start else '-'))
            self.shift_table.setItem(i, 3, QTableWidgetItem(shift.shift_end.strftime('%H:%M') if shift.shift_end else '-'))
            lunch = '-' if not shift.lunch_start or not shift.lunch_end else f"{shift.lunch_start.strftime('%H:%M')} - {shift.lunch_end.strftime('%H:%M')}"
            self.shift_table.setItem(i, 4, QTableWidgetItem(lunch))
            self.shift_table.setItem(i, 5, QTableWidgetItem(f"{shift.hours_worked}h" if shift.hours_worked else '0h'))
            self.shift_table.setItem(i, 6, QTableWidgetItem(shift.status))
        self.shift_table.resizeColumnsToContents()

    def refresh_absences_table(self):
        absences = self.service.get_absences()
        self.absence_table.setRowCount(len(absences))
        for i, absence in enumerate(absences):
            employee = self.service.get_employee(absence.employee_id)
            self.absence_table.setItem(i, 0, QTableWidgetItem(employee.name if employee else "-"))
            self.absence_table.setItem(i, 1, QTableWidgetItem(absence.absence_date.strftime('%Y-%m-%d')))
            self.absence_table.setItem(i, 2, QTableWidgetItem(absence.absence_type))
            self.absence_table.setItem(i, 3, QTableWidgetItem(absence.reason))
            self.absence_table.setItem(i, 4, QTableWidgetItem(absence.half_day or '-'))
            self.absence_table.setItem(i, 5, QTableWidgetItem(f"{absence.salary_deduction:.2f}"))
        self.absence_table.resizeColumnsToContents()

    def refresh_dashboard(self):
        employees = self.service.get_employees()
        total_hours = self.service.get_total_hours()
        total_today = self.service.get_total_hours_today()
        absences = self.service.get_absence_count()

        self.kpi_total_employees.layout().itemAt(0).widget().setText(str(len(employees)))
        self.kpi_total_hours.layout().itemAt(0).widget().setText(f"{total_hours:.1f}h")
        self.kpi_today_hours.layout().itemAt(0).widget().setText(f"{total_today:.1f}h")
        self.kpi_absences.layout().itemAt(0).widget().setText(str(absences))

        summary = self.service.get_employee_hours_summary()
        if summary:
            labels = [name for name, _ in summary[:5]]
            values = [hours for _, hours in summary[:5]]
            self._draw_pie_chart(labels, values)

        daily_rows = self.service.get_total_hours_by_day(14)
        self.daily_table.setRowCount(len(daily_rows))
        for i, item in enumerate(daily_rows):
            self.daily_table.setItem(i, 0, QTableWidgetItem(str(item["date"])))
            self.daily_table.setItem(i, 1, QTableWidgetItem(f"{item['hours']:.1f}h"))

    def _draw_pie_chart(self, labels, values):
        fig = self.chart_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        if values:
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=CHART_COLORS[:len(values)])
            ax.set_title('Horas trabajadas por empleado')
            ax.axis('equal')
        fig.tight_layout()
        self.chart_canvas.draw()

    def closeEvent(self, event):
        self.service.close()
        super().closeEvent(event)
