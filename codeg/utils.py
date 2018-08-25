# 生成文件
from flask_peewee.utils import load_class

from codeg.generate_add_code import generate_add_code
from codeg.generate_edit_code import generate_edit_code
from codeg.generate_model_code import generate_model_code
from codeg.generate_table_code import generate_table_code
import os.path as path
import os

from codeg.generate_view_code import generate_view_code


def _generate_code(template_type, data):

    if template_type == 'model':
        return generate_model_code(data)
    elif template_type == 'add':
        return generate_add_code(data)
    elif template_type == 'table':
        return generate_table_code(data)
    elif template_type == 'edit':
        return generate_edit_code(data)
    elif template_type == 'view':
        return generate_view_code(data)


# 保存文件
def _save_code(template_type, data):
    if template_type == 'model':
        file = _generate_code(template_type, data)
        # print('file\n', file)
        class_name = data['class_name']
        save_path = 'model/%s.py' % class_name
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(file)
    elif template_type == 'add':
        file = _generate_code(template_type, data)
        class_name = data['class_name']
        if not path.exists('templates/%s' % class_name.lower()):
            os.mkdir('templates/%s' % class_name.lower())
        save_path = 'templates/%s/%s.html' % (class_name, class_name.lower() + '_add')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(file)
    elif template_type == 'table':
        file = _generate_code(template_type, data)
        class_name = data['class_name']
        if not path.exists('templates/%s' % class_name.lower()):
            os.mkdir('templates/%s' % class_name.lower())
        save_path = 'templates/%s/%s.html' % (class_name, class_name.lower() + '_table')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(file)
    elif template_type == 'edit':
        file = _generate_code(template_type, data)
        class_name = data['class_name']
        if not path.exists('templates/%s' % class_name.lower()):
            os.mkdir('templates/%s' % class_name.lower())
        save_path = 'templates/%s/%s.html' % (class_name, class_name.lower() + '_edit')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(file)
    elif template_type == 'view':
        file = _generate_code(template_type, data)
        class_name = data['class_name']
        if not path.exists('templates/%s' % class_name.lower()):
            os.mkdir('templates/%s' % class_name.lower())
        save_path = 'templates/%s/%s.html' % (class_name, class_name.lower() + '_view')
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(file)


# 保存文件
def save_code(data):

    _save_code('model', data)
    _save_code('add', data)
    _save_code('table', data)
    _save_code('edit', data)
    _save_code('view', data)


# 删除模型、数据库、页面
def del_model(name):
    # 删除数据库
    klass = load_class('model.' + name + '.' + name)
    klass.drop_table()
    # 删除类文件
    os.remove('model/' + name.capitalize() + '.py')
    # 删除页面文件
    for file in os.listdir('templates/' + name):
        os.remove('templates/' + name + '/' + file)
    # 删除文件夹
    os.removedirs('templates/' + name)