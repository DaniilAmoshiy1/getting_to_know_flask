from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .model_base import SqlAlchemyBase


class Availability(SqlAlchemyBase):
    __tablename__ = 'availability'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey('dishes.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), nullable=False)
    change_date: Mapped[datetime] = mapped_column(nullable=False)
