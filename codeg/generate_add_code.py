def generate_add_code(data):
    inputs = ''
    script = ''
    class_attrs = data['class_attrs']
    class_name = data['class_name']

    for attr in class_attrs:
        field_name = attr['field_name']
        field_type = _get_input_type(attr['field_type'])

        if field_type == 'date':
            script += """
                laydate.render({
                    elem: '#%s'
                });
            """ % field_name
            field_type = 'text'
        elif field_type == 'datetime':
            script += """
                laydate.render({
                    elem: '#%s',
                    type: 'datetime'
                });
            """ % field_name
            field_type = 'text'

        inputs += """
        <div class="layui-form-item">
            <label class="layui-form-label">%s</label>
            <div class="layui-input-block">
                <input id="%s" type="%s" name="%s" required lay-verify="required" autocomplete="off" placeholder="%s" class="layui-input">
            </div>
        </div>
        """ % (field_name, field_name, field_type, field_name, field_name)

    return """<!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <title>编辑</title>
            <link rel="stylesheet" href="../../static/css/layui.css">
        </head>
        <body style="padding-top: 20px; padding-right: 50px;">
        <form name="form" id="form" class="layui-form">
            {# 生成输入框 #}
            %s
            <div class="layui-form-item">
                <div class="layui-input-block">
                    <button class="layui-btn" lay-submit="" lay-filter="model">确定添加</button>
                </div>
            </div>
        </form>
        <script src="../../static/layui.js"></script>
        <script>
            layui.use(['form', 'jquery', 'layer', 'laydate'], function () {
                const form = layui.form;
                const $ = layui.jquery;
                const layer = layui.layer;
                const laydate = layui.laydate;
                
                {# 渲染date #}
                %s
                
                form.on('submit(model)', function(data){
                    layer.open({
                        title: '提示',
                        content:'确定添加数据？',
                        btn: ['确定', '取消'],
                        btn1: function(){
                            $.post({
                                url: '/api/%s/',
                                contentType: 'application/json',
                                data: JSON.stringify(data.field),
                                success: function (data) {
                                    layer.msg('添加成功');
                                    $('#form')[0].reset()
                                }
                            });
                            layer.close(layer.index);
                        },
                    });
                    return false;
                });
            });
        </script>
        </body>
        </html>
            """ % (inputs, script, class_name.lower())


def _get_input_type(raw_type):
    if raw_type == 'IntegerField':
        return 'number'
    elif raw_type == 'FloatField' or raw_type == 'CharField':
        return 'text'
    elif raw_type == 'BooleanField':
        return 'bool'
    elif raw_type == 'DateField':
        return 'date'
    elif raw_type == 'DateTimeField':
        return 'datetime'