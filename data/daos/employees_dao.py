from typing import Optional

from data.db_utilities.session import CafeSession
from data.datamodel.employees import Employees


class EmployeesDao:
    def __init__(self, session=CafeSession.get_session()):
        self.session = session

    def add_employee(self, employee_name, role, mail, phone_number, username, password):
        new_employee = Employees(
            employee_name=employee_name,
            role=role,
            mail=mail,
            phone_number=phone_number,
            username=username,
            password=password
        )
        self.session.add(new_employee)
        self.session.commit()

    def get_all_employees(self):
        return self.session.query(Employees).all()

    def get_employee_by_id(self, employee_id):
        return self.session.query(Employees).filter_by(id=employee_id).first()

    def delete_employee(self, employee_id):
        employee = self.session.query(Employees).get(employee_id)
        if employee:
            self.session.delete(employee)
            self.session.commit()
        else:
            raise ValueError(f'Employee with ID {employee_id} not found')

    def update_employee(
            self,
            employee_id: str,
            employee_name: Optional[str] = None,
            role: Optional[str] = None,
            mail: Optional[str] = None,
            phone_number: Optional[int] = None
    ):
        employee = self.session.query(Employees).filter_by(id=employee_id).first()
        if employee:
            updates = {
                'employee_name': employee_name,
                'role': role,
                'mail': mail,
                'phone_number': phone_number,
            }
            for key, value in updates.items():
                if value is not None:
                    setattr(employee, key, value)

            self.session.commit()
