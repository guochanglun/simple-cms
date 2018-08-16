from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.rest import RestAPI

import setup
from custom import GclAuthentication, GclRestResource
from routes import route

DATABASE = {
    # 数据库名
    'name': 'gcl',
    # 数据库引擎，不用更改
    'engine': 'peewee.MySQLDatabase',
    # 用户名
    'user': 'root',
    # 密码
    'passwd': 'gcl',
}


app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
db = Database(app)
CORS(app, resources='/*')
auth = Auth(app, db)
user_auth = GclAuthentication(auth)
api = RestAPI(app, default_auth=user_auth)


if __name__ == '__main__':
    models = setup.setup()
    # 注册api，发现只有在app.py里注册才能正常使用
    for klass in models:
        api.register(klass, GclRestResource)
    app.register_blueprint(route)
    api.setup()
    app.run()