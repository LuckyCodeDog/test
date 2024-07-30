from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from flask_hashing import Hashing
import re, os
import mysql.connector
from tmb_app import connect
from flask import current_app as app
from functools import wraps
import uuid


common_bp = Blueprint('common', __name__)
# app = create_app()

hashing = Hashing()

# IMPORTANT: Change 'ExampleSaltValue' to whatever salt value you'll use in
# your application. If you don't do this, your password hashes won't work!
PASSWORD_SALT = 'ExampleSaltValue'

# Default role assigned to new users upon registration.
DEFAULT_USER_ROLE = 'member'

db_connection = None

def getCursor():
    """Gets a new dictionary cursor for the database.
    If necessary, a new database connection be created here and used for all
    subsequent to getCursor()."""
    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)

    cursor = db_connection.cursor(dictionary=True)
    return cursor


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if 'username' is in the session to verify if the user is logged in
        if 'id' not in session:
            # If not logged in, redirect to the login page
            return redirect(url_for('common.login'))
        # If logged in, proceed to the original function
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if 'username' is in the session to verify if the user is logged in
            if 'id' not in session:
                # If not logged in, redirect to the login page
                return redirect(url_for('common.login'))
            # Get the user's role from the session
            user_role = session.get('role')
            # Check if the user's role is in the list of required roles
            if user_role not in roles:
                # If the user does not have the required role, return a 403 Forbidden error
                return f("error", 403)
            # If the user has the required role, proceed to the original function
            return f(*args, **kwargs)
        return decorated_function
    return decorator
    


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@common_bp.route('/')
def home():
    return render_template("layout.html")



@common_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']

        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT user_id, username, password_hash, role, firstName, lastName, dob, location, status FROM users WHERE username = %s', (username,))

        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            if account['status']=='inactive':
                flash ('Your account has been frozen!', 'danger')
                return redirect(url_for('common.login'))
            password_hash = account['password_hash']
        #如果找到帐户，则从 account 中提取存储在(数据库)中的密码哈希值.这里的 account 是一个包含用户信息的字典。字典的键是列名，值是相应的列值。
            if hashing.check_value(password_hash, user_password, PASSWORD_SALT):

            # If account exists in accounts table
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['user_id']
                session['username'] = account['username']
                session['role'] = account['role']
                session['firstName'] = account['firstName']
                session['lastName'] = account['lastName']
                session['dob'] = account['dob']
                session['location'] = account['location']


                # Redirect to home page
                if session['role'] == 'member':
                    return redirect(url_for('member.member_home'))
                elif session['role'] == 'moderator':
                    return redirect(url_for('moderator.moderator_home'))
                else:
                    return redirect(url_for('admin.admin_home'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'

    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@common_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''

    # firstname = request.form.get('firstName')
    # lastname = request.form.get('lastName')
    # location = request.form.get('location')      #location = request.form['location']就出错了
    # dob = request.form.get('dob')

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        dob = request.form['dob']
        location = request.form['location']
    #request.form 是类似于字典的对象，但它不是 Python 标准库中的 dict 类型。它实际上是 Werkzeug 库中的 ImmutableMultiDict 类的实例，这是一个不可变的多值字典。

        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesn't exist and the form data is valid, now insert new account into accounts table
            password_hash = hashing.hash_value(password, PASSWORD_SALT)
            cursor.execute('INSERT INTO users (username, password_hash, email, role, firstName, lastName, dob, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                           (username, password_hash, email, DEFAULT_USER_ROLE, firstname, lastname, dob, location))
            db_connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/logout - this will be the logout page
@common_bp.route('/logout')
@login_required
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('role', None)
   session.pop('firstName', None)
   session.pop('lastName', None)
   session.pop('dob', None)
   session.pop('location', None)

   # Redirect to login page
   return redirect(url_for('common.login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@common_bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    # Check if user is loggedin
    # if 'loggedin' not in session:
    #     # User is not logged in - redirect to login page
    #     return redirect(url_for('common.login'))
    # else:
        # We need all the account info for the user so we can display it on the profile page
    user_id = session['id']
    cursor = getCursor()
    cursor.execute('SELECT username, email, role, firstName, lastName, dob, location, status, profile_image FROM users WHERE user_id = %s', (session['id'],))
    account = cursor.fetchone()
    if request.method == 'GET':
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    elif request.method == 'POST':
        action = request.form.get('action')
        if action == 'cancel':
            return redirect(url_for('common.profile'))
        elif action == "save":
            firstname = request.form.get('firstName')
            lastname = request.form.get('lastName')
            email = request.form.get('email')
            dob = request.form.get('dob')
            location = request.form.get('location')

            cursor.execute(
                "UPDATE users set firstname=%s,lastname=%s,email=%s, dob=%s, location=%s "
                "WHERE user_id = %s;", (firstname, lastname, email, dob, location, user_id,))
            # cursor.execute("SELECT firstName, lastName, email, dob, location FROM users  WHERE user_id = %s;", (user_id,))
            flash('Profile updated successfully!')
            return redirect(url_for('common.profile'))
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            cursor.execute('SELECT password_hash FROM users WHERE user_id = %s', (user_id,))
            stored_password_hash = cursor.fetchone()['password_hash']

            if not hashing.check_value(stored_password_hash, current_password, PASSWORD_SALT):
                flash('Current password is incorrect!')
                return redirect(url_for('common.profile'))

            if new_password != confirm_password:
                flash('New passwords do not match!')
                return redirect(url_for('common.profile'))
            new_password_hash = hashing.hash_value(new_password, PASSWORD_SALT)
            cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s', (new_password_hash, user_id))
            flash('Password updated successfully!')
            return redirect(url_for('common.profile', user_id = session['id']))
        elif action == 'replace_image':
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file.filename != '':
                # Generate unique filenames
                    ext=file.filename.rsplit('.', 1)[1]
                    filename = str(uuid.uuid4()) + '.' + ext
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    ######
                    url = url_for('static', filename='profile_images/' + filename)
                    account['profile_image'] = url
                    cursor = getCursor()
                    cursor.execute('''UPDATE users SET profile_image = %s WHERE user_id = %s''', (url, user_id))
                    cursor._rowcount
                    flash('Profile image updated successfully!')
                    return render_template('profile.html', account = account)
                else:
                    flash('No file selected!', 'danger')
                    return render_template('profile.html', account = account)
        elif action == 'remove_image':
            account['profile_image'] = None
            cursor = getCursor()
            cursor.execute('''UPDATE users SET profile_image = null WHERE user_id = %s''', (user_id,))
            cursor._rowcount
            flash('Profile image removed successfully!')
            return render_template('profile.html', account = account)


    