import sqlite3
import hashlib
from paths import DATABASE_PATH

def get_db():#подключение
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):#хешируем пароль
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, name=''):#создание нового юзера
    password_hash = hash_password(password)
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, name))
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        db.close()
        if 'username' in str(e):
            return {'success': False, 'error': 'Такое имя пользователя уже существует!'}
        else:
            return {'success': False, 'error': 'Пользователь с такой почтой уже зарегистрирован!'}

def check_login(email, password):#проверка при входе
    password_hash = hash_password(password)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND password_hash = ?
    ''', (email, password_hash))
    user = cursor.fetchone()
    db.close()
    return user

def get_user_by_id(user_id):#получение данных пользователя по id
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    db.close()
    return user

def get_user_by_email(email):#по email
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    db.close()
    return user

def user_exists(email, username=None):#проверка существования юзера
    db = get_db()
    cursor = db.cursor()
    if username:
        cursor.execute('SELECT id FROM users WHERE email = ? OR username = ?', (email, username))
    else:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    
    exists = cursor.fetchone() is not None
    db.close()
    return exists