from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


# 数据库连接
conn = sqlite3.connect('users2.db')
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    )
''')


@app.route('/')
def index():
    return redirect(url_for('chat'))  # 重定向到聊天页面s



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect('users.db')  # 在函数内创建新连接
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Please choose another one."
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username =?', (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            # 登录成功，设置 Cookie 并跳转聊天页面
            response = make_response(redirect(url_for('chat')))
            response.set_cookie('username', username, max_age=60 * 60 * 24 * 7)
            conn.close()
            return response
        else:
            conn.close()
            return "Invalid username or password."
    return render_template('login.html')



@app.route('/chat')
def chat():
    username = request.cookies.get('username') #获取客户端cookie
    if not username:#判断是否存在cookie
        return redirect(url_for('login')) #不存在cookie，回到登录界面
    if request.method == 'POST': #如果客户端有用表单发送消息
        message = request.form['message'] #获取客户端发送的消息
        print(message)
    return render_template('chat22.html')



@socketio.on('message') #装饰器用于监听名为 message 的事件
def handle_message(data):
    message = data['message']
    username = data['username']
    # 在这里进行数据处理，例如打印、存储到数据库、广播给其他客户端等s
    print(f"收到来自 {username} 的消息: {message}")
    socketio.emit('received_message', {'message': message, 'username': username})

if __name__ == '__main__':
    socketio.run(app,"172.24.130.144",debug=True)