def generate_table_code(data):
    class_name = data['class_name'].lower()
    ths = ''
    class_attrs = data['class_attrs']
    for attr in class_attrs:
        ths += """<th lay-data="{field:'%s', sort: true}">ID</th>""" % attr['field_name']

    return """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="../../static/css/layui.css">
</head>
<body>
<table class="layui-table" lay-filter="demo" lay-data="{height: 'full-20', page: true, limit:20, url:'/api/%s'}">
    <thead>
    <tr>
        {# th #}
        %s
        <th lay-data="{align:'center', toolbar: '#barDemo'}">操作</th>
    </tr>
    </thead>
</table>
<script type="text/html" id="barDemo">
    <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="view">查看</a>
    <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
    <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
</script>
<script src="../../static/layui.js"></script>
<script>
    layui.use(['table', 'layer', 'jquery'], function(){
        const table = layui.table;
        const layer = layui.layer;
        const $ = layui.jquery;
        //监听工具条
        table.on('tool(demo)', function(obj){
            const data = obj.data;
            if(obj.event === 'del'){
                layer.confirm('真的删除行么', function(index){
                    const id = data.id;
                    $.ajax({
                        url: '/api/%s/' + id + '/',
                        type: 'DELETE',
                        success: function(result) {
                            layer.msg('删除成功');
                            obj.del();  
                            layer.close(index);
                        }
                    });
                });
            } else if (obj.event === 'edit') {
                location = '/book/edit/' + data.id
            } else if (obj.event === 'view') {
                location = '/book/view/' + data.id
            }
        });
    });
</script>
</body>
</html>
    """ % (class_name, ths, class_name)