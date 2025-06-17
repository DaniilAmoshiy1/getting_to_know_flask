from functools import wraps
import os

from config import request, session,render_template, Blueprint, app, get_data_from_db, redirect, url_for

from data.db_utilities.session import CafeSession
from data.daos.dishes_dao import DishesDao
from data.datamodel.employees import Employees
from data.daos.employees_dao import EmployeesDao


bp = Blueprint('flask_security', __name__)

app.secret_key = 'key'
roles = ['Owner', 'Administrator', 'Manager', 'Accountant', 'HR-Manager']

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return render_template('identification/login.html', error='You must log in for accept access')
        return func(*args, **kwargs)
    return decorated_function

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username') == 'Roman Voronov':
        return redirect(url_for('employees_control_panel'))
    print(session)
    if 'username' in session:
        return redirect(url_for('categories_control_panel'))
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
    session.pop('role', None)
    return render_template('identification/login.html')


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

@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    image = request.files.get('photo')
    dish_id = request.form.get('dish_id')
    image_folder = os.path.join('static', 'dish_images')

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    image_path = os.path.join(image_folder, f'{dish_id}.png')
    image.save(image_path)

    if not image:
        return 'Error, file not upload', 400

    update_dish = DishesDao()
    update_dish.update_dish(dish_id=dish_id, photo=image_path)

    return redirect(url_for('categories_control_panel'))

@app.route('/employees_control_panel', methods=['GET', 'POST'])
@login_required
def employees_control_panel():
    _, _, employees, _, = get_data_from_db()
    if request.method == 'POST':
        edit_employee = EmployeesDao()
        employees_id = request.form.getlist('employee_ids')
        for employee_id in employees_id:
            new_role = request.form.get(f'role_{employee_id}')
            if new_role:
                edit_employee.update_employee(employee_id=employee_id, role=new_role)

    if session.get('username') == 'Roman Voronov':
        return render_template('identification/employees_control_panel.html', employees=employees, roles=roles)
    else:
        error = 'You do not have access for this page'
        return render_template('identification/login.html', error=error)

@app.route('/availability_control_panel', methods=['GET', 'POST'])
@login_required
def availability_control_panel():
    _, _, _, availability = get_data_from_db()
    return render_template('identification/availability_control_panel.html', availability=availability)
