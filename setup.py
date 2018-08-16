# 启动检查
import os
from flask_peewee.utils import load_class


def _check_model():
    models = []
    # 获取model
    file_list = [name.split('.')[0] for name in os.listdir('./model') if '.py' in name]
    for name in file_list:
        klass = load_class('model.' + name + '.' + name)
        models.append(klass)
        # 检查model中的类，如果数据库中没创建表则创建
        if klass.table_exists():
            # 如果数据库中存在类则删除
            klass.drop_table()
        klass.create_table()

    return models


def setup():
    return _check_model()