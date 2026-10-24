### 一、项目简介
本项目是一个基于Python的后端开发项目，旨在实现一个简单的用户管理系统。项目包括用户注册、登录、个人信息管理等功能。

### 二、项目结构
项目结构如下：
```
backend/
├── app.py
├── models.py
├── routes.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── user.html
└── requirements.txt
```

### 三、项目功能
1. 用户注册：用户可以输入用户名、密码、邮箱等信息进行注册。
2. 用户登录：用户可以输入用户名和密码进行登录。
3. 个人信息管理：用户可以查看和修改自己的个人信息。

### 四、项目运行
1. 创建虚拟环境：
```bash
python3 -m venv .venv
```

2. 激活虚拟环境：
```bash
source .venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行项目：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. uvicorn：命令解释
```
app.main：对应 app/main.py
:app：对应文件中定义的 FastAPI 实例变量 app
--reload：开发时修改代码自动重启
--host 0.0.0.0：监听所有网络接口
--port 8000：使用 8000 端口
```

6. 端口被占用的解决方法：
```bash
lsof -i :8000
kill -9 <PID>
```

### 五、项目说明
1. 项目使用了FastAPI框架进行后端开发。
2. 项目使用了MySQL数据库进行数据存储。

### 六、项目贡献  
如果你有任何建议或发现任何问题，请随时提交issue或PR。感谢你的贡献！


