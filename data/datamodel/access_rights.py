from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .model_base import SqlAlchemyBase

class AccessRights(SqlAlchemyBase):
    __tablename__ = 'access_rights'

    id: Mapped[int] = mapped_column(autoincrement=True, nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), nullable=False )
    role: Mapped[str] = mapped_column(nullable=False)
    right_to_enter_control_panels: Mapped[bool] = mapped_column(nullable=True)
    right_to_edit_categories: Mapped[bool] = mapped_column(nullable=True)
    right_to_edit_dishes: Mapped[bool] = mapped_column(nullable=True)
    right_to_edit_availability: Mapped[bool] = mapped_column(nullable=True)
    right_to_edit_roles: Mapped[bool] = mapped_column(nullable=True)
    right_to_edit_employees_roles: Mapped[bool] = mapped_column(nullable=True)
