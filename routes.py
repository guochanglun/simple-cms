from flask import Blueprint, render_template, request, redirect, url_for
import os, time

from flask_peewee.utils import load_class

from codeg.utils import save_code, del_model

route = Blueprint('route', __name__)
model_list = [name.split('.')[0] for name in os.listdir('./model') if '.py' in name]


# 首页
@route.route("/")
def index():
    return render_template("index.html", model_list=model_list)


# 生成模型
@route.route("/generate_model_del/<name>")
def generate_model_del(name):
    del_model(name)
    return "删除成功"


# 生成模型
@route.route("/generate_model")
def generate_model():
    return render_template("generate_model.html")


# 管理模型
@route.route("/manage_model")
def manage_model():
    # 扫描model文件夹，获取资源名
    file_list = [name.split('.')[0] for name in os.listdir('./model') if '.py' in name]
    return render_template("manage_model.html", res=file_list)


# 保存模型
@route.route('/data', methods=['POST'])
def data():
    params = request.form
    # print(params)
    params_name_list = [*params]
    # print(params_name_list)
    field_list = []
    data = {'class_name': params['class_name'], 'class_attrs': []}
    for params_name in params_name_list:
        if 'field' in params_name:
            field_tag = params_name[11:]
            if field_tag not in field_list:
                field_list.append(field_tag)
                field_attr = {
                    'field_name': params['field_name_' + field_tag],
                    'field_type': params['field_type_' + field_tag],
                    'field_null': params.get('field_null_' + field_tag, 'off'),
                }
                data['class_attrs'].append(field_attr)
    save_code(data)
    return "保存成功"


# 添加
@route.route("/<model>/add")
def add(model):
    return render_template('%s/%s_add.html' % (model, model))


# 添加
@route.route("/<model>/table")
def table(model):
    return render_template('%s/%s_table.html' % (model, model))


# 添加
@route.route("/<model>/edit/<id>")
def edit(model, id):
    klass = load_class('model.%s.%s' % (model.capitalize(), model.capitalize()))
    m = klass.get(id)
    return render_template('%s/%s_edit.html' % (model, model), model = m)


# 查看
@route.route("/<model>/view/<id>")
def view(model, id):
    klass = load_class('model.%s.%s' % (model.capitalize(), model.capitalize()))
    m = klass.get(id)
    return render_template('%s/%s_view.html' % (model, model), model = m)