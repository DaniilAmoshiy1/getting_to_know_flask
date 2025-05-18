from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .model_base import SqlAlchemyBase


class Employees(SqlAlchemyBase):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(autoincrement=True, nullable=False, primary_key=True)
    employee_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    mail: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[Optional[int]] = mapped_column(nullable=True)

    def __repr__(self):
        return (
            f"Employees(id={self.id}, employee_name='{self.employee_name}', role='{self.role}',"
            f"mail='{self.mail}', phone_number={self.phone_number})"
        )

