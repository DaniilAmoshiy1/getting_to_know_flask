from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from passlib.hash import bcrypt

from .model_base import SqlAlchemyBase


class Employees(SqlAlchemyBase, UserMixin):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(autoincrement=True, nullable=False, primary_key=True)
    employee_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=True)
    mail: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[Optional[int]] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    def set_password(self, not_hashed_password):
        self.password = bcrypt.hash(not_hashed_password)

    def check_password(self, not_hashed_password):
        return bcrypt.verify(not_hashed_password, self.password)

    def __repr__(self):
        return (
            f"Employees(id={self.id}, employee_name='{self.employee_name}', role='{self.role}',"
            f"mail='{self.mail}', phone_number={self.phone_number})"
        )

