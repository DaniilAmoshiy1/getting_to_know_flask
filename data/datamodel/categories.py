from sqlalchemy.orm import Mapped, mapped_column

from .model_base import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    category_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"Categories(id={self.id}, category_name='{self.category_name}', description='{self.description}')"
