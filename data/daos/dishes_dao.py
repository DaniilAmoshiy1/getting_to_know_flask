from typing import Optional

from data.db_utilities.session import CafeSession
from data.datamodel.dishes import Dishes


class DishesDao:
    def __init__(self, session=CafeSession.get_session()):
        self.session = session

    def add_dish(
            self,
            dish_name: str,
            photo: bytes,
            price: float,
            category_id: int,
            description: Optional[str] = None
    ):
        new_dish = Dishes(
            dish_name=dish_name,
            description=description,
            photo=photo,
            price=price,
            category_id=category_id
        )
        try:
            self.session.add(new_dish)
            self.session.commit()
        except Exception as add_error:
            self.session.rollback()
            error = f'There was an error adding: {add_error}'

    def get_all_dishes(self):
        return self.session.query(Dishes).all()

    def get_dishes_by_category_id(self, category_id: int):
        return self.session.query(Dishes).filter_by(category_id=category_id).all()

    def delete_dish(self, dish_id: int):
        dish = self.session.query(Dishes).filter_by(id=dish_id).first()
        if dish:
            self.session.delete(dish)
            self.session.commit()
        else:
            raise ValueError(f'Dish with ID {dish_id} not found')

    def update_dish(
            self,
            dish_id: int,
            dish_name: Optional[str] = None,
            photo: Optional[bytes] = None,
            price: Optional[float] = None,
            category_id: Optional[int] = None,
            description: Optional[str] = None
    ):
        dish = self.session.query(Dishes).filter_by(id=dish_id).first()
        if dish:
            updates = {
                'dish_name': dish_name,
                'photo': photo,
                'price': price,
                'category_id': category_id,
                'description': description
            }

            for key, value in updates.items():
                if value is not None:
                    setattr(dish, key, value)

            self.session.commit()
