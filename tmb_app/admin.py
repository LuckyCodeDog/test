from flask import render_template, request
from flask import redirect
from flask import url_for
from flask import session, Blueprint
from tmb_app import create_app, connect
from tmb_app.operations import get_message, get_thread, get_delete_message, get_delete_reply
from tmb_app.db import getCursor
from tmb_app.common import role_required



admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/home', methods=['GET','POST'])
@role_required('admin')
def admin_home():
    # Check if user is loggedin
    # if 'loggedin' in session:
    #     if session['role'] == 'admin':
            # User is loggedin show them the home page and role is admin

    if request.method == 'GET':
    # Handle GET request: display messages
        cursor = getCursor()
        cursor.execute('SELECT message_id, title, content, created_at, messages.user_id, CONCAT(firstName, " ", lastName) AS fullname, profile_image, username FROM messages JOIN users ON messages.user_id = users.user_id ORDER BY created_at DESC')
        #若要在模板中使用 user_id 来进行条件判断（例如，显示删除按钮），需要在SELECT查询中包含 user_id
        user_message_info = cursor.fetchall()
        return render_template('user_home.html', username = session['username'], user_message_info=user_message_info)

    else:
    # Handle POST request: add new message
        cursor = getCursor()
        content = request.form.get('content')  # Get the message content from the form
        title = request.form.get('title')
        if content:
            cursor = getCursor()
            cursor.execute('INSERT INTO messages (title, content, created_at, user_id) VALUES (%s, %s, CURRENT_TIMESTAMP, %s)', (title, content, session['id']))
        return redirect(url_for('admin.admin_home'))
    #     else:
    #         return render_template('Error.html', user_role=session['role'])
        
    # # User is not loggedin redirect to login page
    # return redirect(url_for('login'))




@admin_bp.route('/messages/<int:message_id>', methods=['GET','POST'])
@role_required('admin')
def view_reply_message (message_id):
    return get_thread (message_id, 'admin.view_reply_message')



@admin_bp.route('/delete_message/<int:message_id>', methods=['POST'])
@role_required('admin')
def delete_message (message_id):
    return get_delete_message(message_id, 'admin.admin_home')

@admin_bp.route('/delete_reply/<int:reply_id>', methods=['POST'])
@role_required('admin')
def delete_reply (reply_id):
    return get_delete_reply(reply_id, 'admin.view_reply_message')

@admin_bp.route('/users', methods=['GET','POST'])
@role_required('admin')
def user_management ():
    cursor = getCursor()
    userList = []   #Initialise userList before it's used, regardless of the request method or conditions.
    query = request.args.get('query', '')   #initialise query; default value as an empty string
    if request.method == 'GET':
        if query:   # If query is not empty, the user has entered a search term. Executes search function.
            query = query.strip()
            cursor.execute('''
                            SELECT profile_image, user_id, username, CONCAT(firstName, " ", lastName) AS fullname, email, dob, location, role, status FROM users u
                            WHERE LOWER(u.lastName) like CONCAT('%', %s, '%') 
                            OR LOWER(u.firstName) like CONCAT('%', %s, '%') 
                            OR LOWER(CONCAT(u.firstName, ' ', u.lastName)) LIKE CONCAT('%', %s, '%')
                            OR LOWER(u.username) LIKE CONCAT('%', %s, '%')''', (query, query, query, query))              
        elif query == '':  # If query is empty, no search term is provided. Executes a SQL query to retrieve all users.
            cursor.execute('SELECT profile_image, user_id, username, CONCAT(firstName, " ", lastName) AS fullname, email, dob, location, role, status FROM users')
        userList = cursor.fetchall()
        if not userList:
            print ("No result found")
        return render_template('users.html', username=session['username'], user_role=session['role'], userlist=userList, query=query)
    elif request.method == 'POST':
        user_id = request.form.get('user_id')
        status = request.form.get('status')
        role = request.form.get('role')
        cursor.execute('SELECT role, status FROM users WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()
        # print(type(result))
        existing_role = result['role']
        existing_status = result['status']
        # 当调用cursor.fetchone()多次时：
        # 第一次调用: 返回查询结果的第一行数据，并将游标移动到下一行。
        # 第二次调用: 返回查询结果的第二行数据，并将游标再次移动到下一行。
        # 如果试图从游标中读取超过它包含的数据行的数量，将不会有更多的结果，fetchone()将返回None。
        # 所以需要只调用一次，并从结果中提取所需的数据行
        if status is None:
            status = existing_status
        if role is None:
            role = existing_role
        # Update the user status and role
        cursor.execute('UPDATE users SET status = %s, role = %s WHERE user_id = %s', (status, role, user_id))
        # cursor.commit()
        return redirect(url_for('admin.user_management'))





# inactive会怎样？ admin可以登入moderator吗？ 还是也需要error.html.  所有admin的route都加上session['role']的检查？
#  admin不能把自己设为inactive
