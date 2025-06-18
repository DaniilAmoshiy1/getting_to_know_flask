from data.db_utilities.setup import setup_db, reset_db
from data.daos.categories_dao import CategoriesDao
from data.daos.dishes_dao import DishesDao
from data.daos.employees_dao import EmployeesDao
from data.daos.availability_dao import AvailabilityDao

reset_db()
setup_db()

test_categories = CategoriesDao()
test_dishes = DishesDao()
test_employees = EmployeesDao()
test_availability = AvailabilityDao()

def prefill_database():
    test_categories.create_category('Category 1', 'Something about category')
    test_categories.create_category('Category 2', 'Something about category')
    test_categories.create_category('Category 3', 'Something about category')

    test_dishes.add_dish('Chicken 1', 'path', 1000, 1, 'Buy this')
    test_dishes.add_dish('Chicken 2', 'path', 2000, 2, 'Buy this')
    test_dishes.add_dish('Chicken 3', 'path', 3000, 3, 'Buy this')

    test_employees.add_employee('DetektivKote', 'Administrator', 'mail@gmail.com', '88005553535', 'DetektivKote', 3241)
    test_employees.add_employee('DetektivKote2', 'Administrator', 'mail@gmail.com', '88005553535', 'DetektivKote2', 3241)
    test_employees.add_employee('DetektivKote3', 'Administrator', 'mail@gmail.com', '88005553535', 'DetektivKote3', 3241)

    test_availability.create_availability(True, 1, 1)
    test_availability.create_availability(True, 2, 2)
    test_availability.create_availability(False, 3, 3)

prefill_database()
