from typing import Optional

from data.db_utilities.session import CafeSession
from data.datamodel.availability import Availability


class AvailabilityDao:
    def __init__(self, session=CafeSession.get_session()):
        self.session = session

    def create_availability(
            self,
            is_active: bool,
            dish_id: int,
            user_id: int
    ):
        new_availability = Availability(
            is_active=is_active,
            dish_id=dish_id,
            user_id=user_id
        )
        self.session.add(new_availability)
        self.session.commit()

    def read_availability(self):
        return self.session.query(Availability).all()

    def delete_availability(self, availability_id):
        availability = self.session.query(Availability).filter_by(id=availability_id).first()
        if availability:
            self.session.delete(availability)
            self.session.commit()
        else:
            raise ValueError(f'Availability with ID {availability_id} not found')

    def update_availability(
            self,
            availability_id: int,
            is_active: bool,
            dish_id: int,
            user_id: int,
    ):
        availability = self.session.query(Availability).filter_by(id=availability_id).first()
        if availability:
            updates = {
                'is_active': is_active,
                'dish_id': dish_id,
                'user_id': user_id
            }
            for key, value in updates.items():
                if value is not None:
                    setattr(availability, key, value)

            self.session.commit()
        else:
            raise ValueError(f'{availability_id} does not exist in this table')
