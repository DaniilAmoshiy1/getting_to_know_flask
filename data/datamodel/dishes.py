from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKey

from .model_base import SqlAlchemyBase


class Dishes(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dish_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )

    def __repr__(self):
        return (
            f"Dishes(id={self.id}, dish_name='{self.dish_name}', description='{self.description}',"
            f"photo={self.photo} price={self.price}, category_id={self.category_id})"
        )
