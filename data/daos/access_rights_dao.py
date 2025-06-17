from typing import Optional


from data.db_utilities.session import CafeSession
from data.datamodel.access_rights import AccessRights


class AvailabilityDao:
    def __init__(self, session=CafeSession.get_session()):
        self.session = session

    def add_access_rights(
            self,
            employee_id: int,
            role: str,
            right_to_enter_control_panels: Optional[bool] = None,
            right_to_edit_categories: Optional[bool] = None,
            right_to_edit_dishes: Optional[bool] = None,
            right_to_edit_availability: Optional[bool] = None,
            right_to_edit_roles: Optional[bool] = None,
            right_to_edit_employees_roles: Optional[bool] = None
    ):
        new_access_rights = AccessRights(
            employee_id=employee_id,
            role=role,
            right_to_enter_control_panels=right_to_enter_control_panels,
            right_to_edit_categories=right_to_edit_categories,
            right_to_edit_dishes=right_to_edit_dishes,
            right_to_edit_availability=right_to_edit_availability,
            right_to_edit_roles=right_to_edit_roles,
            right_to_edit_employees_roles=right_to_edit_employees_roles
        )
        try:
            self.session.add(new_access_rights)
            self.session.commit()
        except Exception as add_rights_error:
            self.session.rollback()
            error = add_rights_error

    def read_access_rights(self):
        return self.session.query(AccessRights).all()

    def delete_role(self, role_id):
        role = self.session.query(AccessRights).filter_by(id=role_id).first()
        if role:
            self.session.delete(role)
            self.session.commit()
        else:
            raise ValueError(f'Role with ID {role_id} not found')

    def update_role(
            self,
            role_id: int,
            role: str,
            right_to_enter_control_panels: Optional[bool] = None,
            right_to_edit_categories: Optional[bool] = None,
            right_to_edit_dishes: Optional[bool] = None,
            right_to_edit_availability: Optional[bool] = None,
            right_to_edit_roles: Optional[bool] = None,
            right_to_edit_employees_roles: Optional[bool] = None
    ):
        role_check = self.session.query(AccessRights).filter_by(id=role_id).first()
        if role_check:
            updates = {
                'role': role,
                'right_to_enter_control_panels': right_to_enter_control_panels,
                'right_to_edit_categories': right_to_edit_categories,
                'right_to_edit_dishes': right_to_edit_dishes,
                'right_to_edit_availability': right_to_edit_availability,
                'right_to_edit_roles': right_to_edit_roles,
                'right_to_edit_employees_roles': right_to_edit_employees_roles,
            }
            for key, value in updates.items():
                if value is not None:
                    setattr(role_check, key, value)

            self.session.commit()
        else:
            raise ValueError(f'{role_id} does not exist in this table')




