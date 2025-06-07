from functools import wraps

from config import request, session,render_template, Blueprint, app, get_data_from_db

from data.db_utilities.session import CafeSession
from data.datamodel.employees import Employees
from data.daos.dishes_dao import DishesDao


bp = Blueprint('flask_security', __name__)

app.secret_key = 'key'

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    db_session = CafeSession.get_session()
    check_user = db_session.query(Employees).filter_by(username=username).first()

    categories, _, _, _, = get_data_from_db()
    if check_user and check_user.check_password(password):
        session.permanent = True
        session['username'] = username
        return render_template('identification/categories_control_panel.html', categories=categories)
    else:
        return render_template('identification/login.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('identification/register.html')

    full_name = request.form.get('full_name')
    role = None
    user_mail = request.form.get('user_mail')
    phone_number = request.form.get('phone_number')
    username = request.form.get('username')
    password = request.form.get('password')

    if not password:
        return render_template('identification/register.html', error='Error: Password not transmitted!')

    db_session = CafeSession.get_session()
    check_user = db_session.query(Employees).filter_by(username=username).first()
    if check_user:
        return render_template('identification/register.html', error='The user already exists')

    new_employee = Employees(
        employee_name=full_name,
        role=role,
        mail=user_mail,
        phone_number=phone_number,
        username=username
    )
    new_employee.set_password(password)

    db_session.add(new_employee)
    db_session.commit()
    db_session.close()

    return render_template('identification/login.html')


# logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('identification/login.html')


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return render_template('identification/login.html', error='You must log in for accept access')
        return func(*args, **kwargs)
    return decorated_function

@app.route('/categories_control_panel')
@login_required
def categories_control_panel():
    print(session.get('username'))
    categories, _, _, _, = get_data_from_db()
    return render_template('identification/categories_control_panel.html', categories=categories)

@app.route('/dishes_control_panel', methods=['GET', 'POST'])
@login_required
def dishes_control_panel():
    print(session.get('username'))
    dish_dao = DishesDao()
    find_dishes = request.args.get('find_dishes')
    print(find_dishes)
    categories, dishes, _, _, = get_data_from_db()
    key = [key for key, value in categories.items() if value[0] == find_dishes]
    for number in key:
        key = number
    for keys, values in dishes.items():
        if key == values[4]:
            dishes_list = dish_dao.get_dishes_by_category_id(key)
            dishes_dict = {dish.id: [dish.dish_name, dish.description, dish.photo, dish.price] for dish in dishes_list}
            return render_template('identification/dishes_control_panel.html', dishes=dishes_dict)
