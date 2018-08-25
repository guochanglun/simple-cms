def generate_edit_code(data):
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
                <input id="%s" value="{{ model.%s }}" type="%s" name="%s" required lay-verify="required" autocomplete="off" placeholder="%s" class="layui-input">
            </div>
        </div>
        """ % (field_name, field_name, field_name, field_type, field_name, field_name)

    return """<!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <title>编辑</title>
            <link rel="stylesheet" href="../../static/css/layui.css">
        </head>
        <body style="padding-top: 20px;">
        <form name="form" id="form" class="layui-form">
            {# 生成输入框 #}
            <input type="hidden" name="id" value={{ model.id }} />
            %s
            <div class="layui-form-item">
                <div class="layui-input-block">
                    <a href="/%s/table" class="layui-btn">返回列表</a>
                    <button class="layui-btn" lay-submit="" lay-filter="model">确定修改</button>
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
                            $.ajax({
                                url: '/api/%s/',
                                type: 'post',
                                contentType: 'application/json',
                                data: JSON.stringify(data.field),
                                success: function (data) {
                                    location = '/%s/table';
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
            """ % (inputs, class_name.lower(), script, class_name.lower(), class_name.lower())


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