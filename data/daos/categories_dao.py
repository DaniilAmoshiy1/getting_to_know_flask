from typing import Optional

from data.db_utilities.session import CafeSession
from data.datamodel.categories import Categories


class CategoriesDao:
    def __init__(self, session=CafeSession.get_session()):
        self.session = session

    def create_category(self, category_name: str, description: Optional[str] = None):
        new_category = Categories(category_name=category_name, description=description)
        try:
            self.session.add(new_category)
            self.session.commit()
        except Exception as add_error:
            self.session.rollback()
            error = f'There was an error adding: {add_error}'

    def read_categories(self):
        return self.session.query(Categories).all()

    def delete_category(self, category_id):
        category = self.session.query(Categories).filter_by(id=category_id).first()
        if category:
            self.session.delete(category)
            self.session.commit()
        else:
            raise ValueError(f'Category with ID {category_id} not found')

    def update_category(
            self,
            category_id: int,
            category_name: Optional[str] = None,
            description: Optional[str] = None
    ):
        category = self.session.query(Categories).filter_by(id=category_id).first()
        if category:
            updates = {
                'category_name': category_name,
                'description': description
            }

            for key, value in updates.items():
                if value is not None:
                    setattr(category, key, value)

            self.session.commit()
        else:
            raise ValueError(f'{category_id} does not exist in this table')
