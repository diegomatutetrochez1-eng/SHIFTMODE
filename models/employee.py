"""
Modelo de Empleado
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from config.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)
    position = Column(String(100), nullable=True)
    hire_date = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "position": self.position,
            "hire_date": self.hire_date,
            "is_active": self.is_active,
        }
