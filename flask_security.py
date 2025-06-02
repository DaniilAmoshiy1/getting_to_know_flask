from flask import request, session, redirect, url_for, render_template
from flask_login import LoginManager

from main import app
from data.db_utilities.session import CafeSession
from data.datamodel.employees import Employees
from data.daos.employees_dao import EmployeesDao

app.secret_key = 'key'
print('Login manager not created')
login_manager = LoginManager()
print('Login manager created')
login_manager.init_app(app)


# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form(['username'])
    password = request.form(['password'])
    db_session = CafeSession.get_session()
    check_user = db_session.query(Employees).filter_by(username=username).first()
    if check_user and check_user.check_password(password):
        session['username'] = username
        return redirect(url_for('control_panel'))
    else:
        return render_template('login.html')

# register
@app.route('/register')
def register():
    full_name = request.form(['full_name'])
    role = None
    user_mail = request.form(['user_mail'])
    phone_number = request.form(['phone_number'])
    username = request.form(['username'])
    password = request.form(['password'])
    EmployeesDao.add_employee(
        full_name,
        role,
        user_mail,
        phone_number,
        username,
        password
    )
    return render_template('login.html')

# logout

