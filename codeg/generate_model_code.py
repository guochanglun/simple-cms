def generate_model_code(data):
    # 生成属性对象
    fields = ''
    class_attrs = data['class_attrs']
    for attr in class_attrs:
        field_null = 'True'
        if attr['field_null'] == 'off':
            field_null = 'False'

        fields += '''
    # %s
    %s = %s(null=%s)''' % (attr['field_name'], attr['field_name'], attr['field_type'], field_null)
    # print('generate_model_code----------------------')
    return '''from app import db
from peewee import CharField, IntegerField, BooleanField, DateTimeField, DateField, FloatField


class %s(db.Model):
    %s''' % (data['class_name'], fields)