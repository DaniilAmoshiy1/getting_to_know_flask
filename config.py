from flask import (
    Flask,
    Request,
    render_template,
    request,
    session,
    redirect,
    url_for,
    Blueprint
)

from data.db_utilities.session import CafeSession
from data.datamodel.categories import Categories
from data.datamodel.dishes import Dishes
from data.datamodel.employees import Employees
from data.datamodel.availability import Availability

app = Flask(__name__)


def get_data_from_db():
    with CafeSession.get_session() as sess:
        categories_db = sess.query(Categories).all()
        categories = {category.id: [category.category_name, category.description] for category in categories_db}
        dishes_db = sess.query(Dishes).all()
        dishes = {
            dishes.id: [
                dishes.dish_name,
                dishes.description,
                dishes.photo,
                dishes.price,
                dishes.category_id
            ] for dishes in dishes_db
        }
        employees = sess.query(Employees).all()
        availability = sess.query(Availability).all()
    return categories, dishes, employees, availability
