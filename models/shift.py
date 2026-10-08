"""
Modelo de Jornada Laboral
"""
from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey, Text
from datetime import datetime
from config.database import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_date = Column(DateTime, default=datetime.now)
    shift_start = Column(DateTime, nullable=True)
    shift_end = Column(DateTime, nullable=True)
    lunch_start = Column(DateTime, nullable=True)
    lunch_end = Column(DateTime, nullable=True)
    hours_worked = Column(Float, default=0.0)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "shift_date": self.shift_date,
            "shift_start": self.shift_start,
            "shift_end": self.shift_end,
            "lunch_start": self.lunch_start,
            "lunch_end": self.lunch_end,
            "hours_worked": self.hours_worked,
            "status": self.status,
        }


class Absence(Base):
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    absence_date = Column(DateTime, nullable=False)
    reason = Column(String(255), nullable=False)
    absence_type = Column(String(50), nullable=False)
    half_day = Column(String(20), nullable=True)
    salary_deduction = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "absence_date": self.absence_date,
            "reason": self.reason,
            "absence_type": self.absence_type,
            "half_day": self.half_day,
            "salary_deduction": self.salary_deduction,
            "notes": self.notes,
        }
