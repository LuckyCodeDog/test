
from tmb_app import connect
import mysql.connector

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