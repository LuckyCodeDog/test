from flask import render_template
from flask import redirect, request
from flask import url_for
from flask import session, Blueprint
from tmb_app import create_app, connect
from tmb_app.db import getCursor
from tmb_app.operations import get_message, get_thread, get_delete_message, get_delete_reply
import mysql.connector
from tmb_app.common import role_required

# app = create_app()

moderator_bp = Blueprint('moderator', __name__)

# db_connection = None

# def getCursor():
#     """Gets a new dictionary cursor for the database.

#     If necessary, a new database connection be created here and used for all
#     subsequent to getCursor()."""
#     global db_connection

#     if db_connection is None or not db_connection.is_connected():
#         db_connection = mysql.connector.connect(user=connect.dbuser, \
#             password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
#             database=connect.dbname, autocommit=True)

#     cursor = db_connection.cursor(dictionary=True)

#     return cursor

@moderator_bp.route('/home', methods=['GET', 'POST'])
@role_required('moderator')
def moderator_home():
    # Check if user is loggedin
    # if 'loggedin' in session:
        # User is loggedin show them the home page
    return get_message('user_home.html', 'moderator.moderator_home')
    
    # User is not loggedin redirect to login page
    # return redirect(url_for('common.login'))



@moderator_bp.route('/messages/<int:message_id>', methods=['GET','POST'])
@role_required('moderator')
def view_reply_message (message_id):
    return get_thread (message_id, 'moderator.view_reply_message')
    # if 'loggedin' not in session:
    #     return redirect(url_for('common.login'))

    # elif 'loggedin' in session:
    #     user_id = session['id']
    #     if request.method == 'POST':
    #         # app.logger.info('Handling POST request for message_id: %s', message_id)
    #         content = request.form.get('content')
    #         if content:
    #             cursor = getCursor()
    #             cursor.execute('INSERT INTO replies (content, user_id, message_id) VALUES (%s, %s, %s)', (content, user_id, message_id))
    #             db_connection.commit()
    #         return redirect(url_for('moderator.view_reply_message', message_id=message_id))
    #         # Redirect to the same page to display the updated thread.
    #     elif request.method == 'GET':
    #         # app.logger.info('Handling GET request for message_id: %s', message_id)

    #         # Handle GET request: display individual message thread
    #         cursor = getCursor()
    #         cursor.execute('''
    #             SELECT
    #                 r.reply_id, 
    #                 m.message_id, 
    #                 m.title, 
    #                 m.content AS message_content, 
    #                 r.content AS reply_content, 
    #                 m.created_at AS message_created_at, 
    #                 r.created_at AS reply_created_at, 
    #                 r.user_id AS reply_user_id,
    #                 ru.firstName AS reply_user_first_name,
    #                 ru.lastName AS reply_user_last_name,
	# 				m.user_id AS message_user_id,
	# 				mu.firstName AS message_user_first_name,
	# 				mu.lastName AS message_user_last_name,
	# 				CONCAT(ru.firstName, ' ', ru.lastName) AS reply_fullname,
    #                 CONCAT(mu.firstName, ' ', mu.lastName) AS msg_fullname
    #             FROM 
    #                 messages AS m
    #             LEFT JOIN   
    #                 # 否则，r.message_id为空的时候，thread_detail也会是空置
    #                 replies AS r ON m.message_id = r.message_id
	# 			LEFT JOIN
	# 				users AS ru ON r.user_id = ru.user_id
	# 			LEFT JOIN
	# 				users AS mu ON m.user_id = mu.user_id  
    #             WHERE 
    #                 m.message_id = %s
    #             # 这里也很重要，不能是r.message_id
    #             ORDER BY 
    #                 r.created_at DESC
    #             LIMIT 
    #                 0, 1000
    #             ''', (message_id,))



    #         #若要在模板中使用 user_id 来进行条件判断（例如，显示删除按钮），需要在SELECT查询中包含 user_id

    #         thread_detail = cursor.fetchall()

    #         return render_template('mod_ad_thread.html', username=session['username'], user_role=session['role'], thread_detail = thread_detail, message_id=message_id)












@moderator_bp.route('/delete_message/<int:message_id>', methods=['POST'])
@role_required('moderator')
def delete_message (message_id):
    return get_delete_message(message_id, 'moderator.moderator_home')
# def delete_message (message_id):   #如果 msg_id 不是表单数据，但你仍然想通过 URL 参数传递它，你可以将模板中的删除按钮结构化，以将 msg_id 作为 URL 的一部分。
#     cursor = getCursor()

#     cursor.execute('DELETE FROM replies WHERE message_id = %s', (message_id,))
#     cursor.execute('DELETE FROM messages WHERE message_id = %s', (message_id,))

#     app.logger.info('hello world delete message')
#     return redirect(url_for('moderator.moderator_home'))
    #当你提交一个删除请求时，浏览器会发送一个 POST 请求。如果你在处理完删除操作后直接返回一个 HTML 页面（使用 render_template），用户可能会面临页面刷新时重新提交表单的提示。这是因为浏览器会重新发送最后一个请求，导致重复的删除操作。
    # 重定向是一种更好的实践：通过使用 redirect 和 url_for，你可以重定向用户到另一个视图函数。这不仅避免了表单重新提交问题，还能使 URL 更加友好和清晰。
    # 在 Flask 的 redirect 函数中，不能直接传递 username 和 user_role 作为参数，你应该将这些数据传递到目标视图函数中。

@moderator_bp.route('/delete_reply/<int:reply_id>', methods=['POST'])
@role_required('moderator')
def delete_reply (reply_id):
    return get_delete_reply(reply_id, 'moderator.view_reply_message')
# cursor = getCursor()
#     cursor.execute('SELECT message_id FROM replies WHERE reply_id = %s', (reply_id,))
#     result = cursor.fetchone()
#     message_id = int(result['message_id'])   # result是一个字典
#     cursor.execute('DELETE FROM replies WHERE reply_id = %s', (reply_id,))
#     return redirect(url_for('moderator.view_reply_message', message_id=message_id))

