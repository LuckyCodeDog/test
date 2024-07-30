# from flask import Flask
#
# app = Flask(__name__)
# app.secret_key = 'Example Secret Key (Change this!)'
#
# from tmb_app import member
# from tmb_app import moderator
# from tmb_app import admin

from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Example Secret Key (Change this!)'
    app.config['UPLOAD_FOLDER'] = 'tmb_app/static/profile_images'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    return app


#__init__.py 文件通常位于一个 Python 包（即一个包含模块的目录）的根目录中。它的主要作用如下：
# 标识包：
# __init__.py 文件用于将一个目录标识为一个 Python 包。没有这个文件，Python 将不会将该目录识别为包，这意味着你无法从该目录导入模块。
# 包初始化：
# __init__.py 文件可以包含初始化代码，当包被导入时会执行这些代码。通常，它用于设置包的全局变量、导入子模块等。
# 在你的 Flask 应用中，__init__.py 文件用于创建和配置 Flask 应用实例，并导入应用的各个蓝图或模块。