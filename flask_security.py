from config import request, session,render_template, Blueprint, app, get_data_from_db

from data.db_utilities.session import CafeSession
from data.datamodel.employees import Employees


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
        session['username'] = username
        return render_template('control_panel.html', categories=categories)
    else:
        return render_template('login.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    full_name = request.form.get('full_name')
    role = None
    user_mail = request.form.get('user_mail')
    phone_number = request.form.get('phone_number')
    username = request.form.get('username')
    password = request.form.get('password')

    if not password:
        return render_template('register.html', error='Error: Password not transmitted!')

    db_session = CafeSession.get_session()
    check_user = db_session.query(Employees).filter_by(username=username).first()
    if check_user:
        return render_template('register.html', error='The user already exists')

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

    return render_template('login.html')


# logout

