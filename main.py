from config import render_template, request, app, get_data_from_db

from data.db_utilities.setup import setup_db, reset_db
from data.daos.categories_dao import CategoriesDao
from data.daos.dishes_dao import DishesDao
from flask_security import bp


app.register_blueprint(bp)

reset_db()
setup_db()

@app.route('/', methods=['GET'])
def get_links():
    return render_template('main_links.html')

@app.route('/categories', methods=['GET'])
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
    new_dishes.add_dish('Говядина', None, 2000, 1, 'Это вкусно, купите')
    new_dishes.add_dish('Кто то ещё', None, 2000, 2, 'Это вкусно, купите')
    find_dishes = request.args.get('find_dishes')
    categories, dishes, _, _, = get_data_from_db()
    key = [key for key, value in categories.items() if value[0] == find_dishes]
    for number in key:
        key = number
    for keys, values in dishes.items():
        if key == values[4]:
            dishes_list = new_dishes.get_dishes_by_category_id(key)
            dishes_dict = {dish.id: [dish.dish_name, dish.description, dish.photo, dish.price] for dish in dishes_list}
            return render_template('dishes.html', dishes=dishes_dict)


if __name__ == '__main__':
    app.run(debug=True)
