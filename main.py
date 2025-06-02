from flask import Flask, Request, render_template, request

from data.db_utilities.session import CafeSession
from data.datamodel.categories import Categories
from data.datamodel.dishes import Dishes
from data.datamodel.employees import Employees
from data.datamodel.availability import Availability
from data.db_utilities.setup import setup_db, reset_db
from data.daos.categories_dao import CategoriesDao
from data.daos.dishes_dao import DishesDao


app = Flask(__name__)

def get_data_from_db():
    with CafeSession.get_session() as session:
        categories_db = session.query(Categories).all()
        categories = {category.id: [category.category_name, category.description] for category in categories_db}
        dishes_db = session.query(Dishes).all()
        dishes = {
            dishes.id: [
                dishes.dish_name,
                dishes.description,
                dishes.photo,
                dishes.price,
                dishes.category_id
            ] for dishes in dishes_db
        }
        employees = session.query(Employees).all()
        availability = session.query(Availability).all()
    return categories, dishes, employees, availability


@app.route('/')
def get_links():
    reset_db()
    setup_db()
    return render_template('main_links.html')

@app.route('/categories')
def get_categories():
    new_category = CategoriesDao()
    new_category.create_category('First category', 'Kva')
    new_category.create_category('Second category', 'Kva2')
    categories, _, _, _, = get_data_from_db()
    return render_template(
        'categories.html',
        categories=categories
    )

@app.route('/get_dishes', methods=['GET'])
def get_dishes():
    new_dishes = DishesDao()
    new_dishes.add_dish('Жареные яйца', None, 2000, 1, 'Это вкусно, купите')
    new_dishes.add_dish('Сырая курица', None, 2000, 2, 'Это вкусно, купите')
    new_dishes.add_dish('Попа кота', None, 2000, 1, 'Это вкусно, купите')
    new_dishes.add_dish('Хвост кобылы', None, 2000, 2, 'Это вкусно, купите')
    find_dishes = request.args.get('find_dishes')
    print(find_dishes)
    categories, dishes, _, _, = get_data_from_db()
    key = [key for key, value in categories.items() if value[0] == find_dishes]
    for number in key:
        key = number
    for keys, values in dishes.items():
        if key == values[4]:
            dishes_list = new_dishes.get_dishes_by_category_id(key)
            dishes_dict = {dish.id: [dish.dish_name, dish.description, dish.photo, dish.price] for dish in dishes_list}
            # print(f'Dishes list = {dishes_list}')
            # print(f'Dishes dict = {dishes_dict}')
            return render_template('dishes.html', dishes=dishes_dict)


if __name__ == "__main__":
    app.run(debug=True)
