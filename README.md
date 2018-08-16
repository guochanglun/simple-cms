# simple-cms
简单的cms生成器

### 用到的框架
1. 前端使用layui
2. 后端使用flask, peewee, flask-peewee
3. 为了适应layui table的数据要求，对flask-peewee的RestResource类进行了继承修改

### 使用方法

#### 配置mysql数据库
在app.py修改数据库参数
```python
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
```

#### 启动

启动app.py即可：python app.py

#### 创建资源模型

1. 打开1270.0.1:5000
2. 点击侧边栏按钮 “添加资源模型”
3. 操作页面添加资源模型
4. 重启app.py，程序会自动为添加的资源创建数据库表和增删改查页面
5. 再次进入1270.0.1:5000，会发现侧边栏多出了一些菜单

### 项目目录
```text
simple-cms
    - codeg: 生成和资源相关的代码和页面
        - generate_add_code.py: 生成资源添加页面
        - generate_edit_code.py: 生成资源编辑页面
        - generate_table_code.py: 生成资源列表页面
        - generate_view_code.py: 生成资源查看页面
        - utils.py: 整合以上功能，对外提供方法
    - model: 保存生成的模型
    - static: flask静态资源目录
    - templates：flask页面模板目录
        - generate_model.html: 模型生成页面
        - index.html：首页
    - app.py: 项目入口，启动文件
    - custom.py：对flask—peewee框架的自定义修改
    - routes.py: flask路由文件
    - setup.py: 启动时检查模型和创建数据库表
```

### 注意
为了方便看到效果，在setup.py中写的时每次启动重新删除表再创建，如果表存在不删除的话可以修改代码
```python
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
```

### 遇到的问题

#### flask-peewee的坑
1. 更新的api比如：post:/api/book，不能进行更新，反而会redirect到get:/api/book，并且这个redirect只是在debug模式下才会报错，也就是说在非debug模式下跳转了你也不知道，大坑！
修改api为post:/api/book/可以解决问题，没错，多加了一个'/'
2. flask-peewee的post和put更新数据只能接受json提交的表单，使用一般的form提交表单会报错，
可以使用jquery.ajax指定contentType为application/json或text/plain都可以，并且同时要求你的data是json格式的

### 继续...
程序没完成，缺少用户和权限，以后再慢慢完成