from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from config.database import get_session
from models.employee import Employee
from models.shift import Absence, Shift


class DataService:
    def __init__(self):
        self.session = get_session()

    def close(self):
        if self.session:
            self.session.close()

    def create_employee(self, name, email, phone=None, address=None, position=None):
        employee = Employee(
            name=name,
            email=email,
            phone=phone,
            address=address,
            position=position,
        )
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_employees(self):
        return self.session.query(Employee).order_by(Employee.name.asc()).all()

    def get_employee(self, employee_id):
        return self.session.query(Employee).filter(Employee.id == employee_id).first()

    def delete_employee(self, employee_id):
        employee = self.get_employee(employee_id)
        if employee:
            self.session.delete(employee)
            self.session.commit()
            return True
        return False

    def get_employee_details(self, employee_id):
        employee = self.get_employee(employee_id)
        if not employee:
            return None

        latest_shift = self.session.query(Shift).filter(Shift.employee_id == employee_id).order_by(Shift.shift_date.desc()).first()
        return {
            "employee": employee,
            "latest_shift": latest_shift,
        }

    def start_shift(self, employee_id):
        active_shift = self.session.query(Shift).filter(
            Shift.employee_id == employee_id,
            Shift.status == "in_progress",
        ).first()
        if active_shift:
            return active_shift

        shift = Shift(
            employee_id=employee_id,
            shift_date=datetime.now(),
            shift_start=datetime.now(),
            status="in_progress",
        )
        self.session.add(shift)
        self.session.commit()
        self.session.refresh(shift)
        return shift

    def lunch_start(self, employee_id):
        active_shift = self.session.query(Shift).filter(
            Shift.employee_id == employee_id,
            Shift.status == "in_progress",
        ).order_by(Shift.id.desc()).first()
        if not active_shift:
            return None
        if active_shift.lunch_start:
            return active_shift
        active_shift.lunch_start = datetime.now()
        self.session.commit()
        return active_shift

    def lunch_end(self, employee_id):
        active_shift = self.session.query(Shift).filter(
            Shift.employee_id == employee_id,
            Shift.status == "in_progress",
        ).order_by(Shift.id.desc()).first()
        if not active_shift:
            return None
        if active_shift.lunch_end:
            return active_shift
        active_shift.lunch_end = datetime.now()
        self.session.commit()
        return active_shift

    def end_shift(self, employee_id):
        active_shift = self.session.query(Shift).filter(
            Shift.employee_id == employee_id,
            Shift.status == "in_progress",
        ).order_by(Shift.id.desc()).first()
        if not active_shift:
            return None

        end_time = datetime.now()
        active_shift.shift_end = end_time
        active_shift.status = "completed"

        # Cálculo de horas trabajadas con descanso de almuerzo
        start = active_shift.shift_start
        if start is None:
            start = end_time

        total_seconds = (end_time - start).total_seconds()

        if active_shift.lunch_start and active_shift.lunch_end:
            lunch_seconds = (active_shift.lunch_end - active_shift.lunch_start).total_seconds()
            total_seconds -= max(0, lunch_seconds)

        active_shift.hours_worked = round(max(0, total_seconds) / 3600, 2)
        self.session.commit()
        self.session.refresh(active_shift)
        return active_shift

    def get_last_n_shifts(self, limit=20):
        return self.session.query(Shift).order_by(Shift.shift_date.desc()).limit(limit).all()

    def get_shifts_for_employee(self, employee_id):
        return self.session.query(Shift).filter(Shift.employee_id == employee_id).order_by(Shift.shift_date.desc()).all()

    def add_absence(self, employee_id, absence_date, reason, absence_type, half_day=None, salary_deduction=0.0, notes=None):
        absence = Absence(
            employee_id=employee_id,
            absence_date=absence_date,
            reason=reason,
            absence_type=absence_type,
            half_day=half_day,
            salary_deduction=salary_deduction,
            notes=notes,
        )
        self.session.add(absence)
        self.session.commit()
        self.session.refresh(absence)
        return absence

    def get_absences(self):
        return self.session.query(Absence).order_by(Absence.absence_date.desc()).all()

    def get_absences_for_employee(self, employee_id):
        return self.session.query(Absence).filter(Absence.employee_id == employee_id).order_by(Absence.absence_date.desc()).all()

    def get_total_hours(self):
        result = self.session.query(func.coalesce(func.sum(Shift.hours_worked), 0)).scalar()
        return float(result or 0)

    def get_total_hours_today(self):
        today = datetime.now().date()
        result = self.session.query(func.coalesce(func.sum(Shift.hours_worked), 0)).filter(
            func.date(Shift.shift_date) == today
        ).scalar()
        return float(result or 0)

    def get_employee_hours_summary(self):
        rows = self.session.query(Employee.name, func.coalesce(func.sum(Shift.hours_worked), 0).label("hours")).outerjoin(
            Shift, Employee.id == Shift.employee_id
        ).group_by(Employee.id).order_by(func.sum(Shift.hours_worked).desc()).all()
        return [(name, float(hours or 0)) for name, hours in rows]

    def get_total_hours_by_day(self, days=14):
        from datetime import timedelta
        start = datetime.now().date() - timedelta(days=days)
        rows = self.session.query(
            func.date(Shift.shift_date).label("day"),
            func.coalesce(func.sum(Shift.hours_worked), 0).label("hours")
        ).filter(func.date(Shift.shift_date) >= start).group_by(func.date(Shift.shift_date)).order_by(func.date(Shift.shift_date)).all()

        result = []
        for day, hours in rows:
            result.append({
                "date": day,
                "hours": float(hours or 0),
            })
        return result

    def get_employee_count(self):
        return self.session.query(Employee).count()

    def get_absence_count(self):
        return self.session.query(Absence).count()
