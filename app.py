from flask import Flask, render_template, request, redirect, flash, url_for, session
from database import create_user, check_login, get_user_by_id, user_exists
from paths import PROJECT_ROOT, DATABASE_PATH
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-12345'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-quiz')
def create_quiz():
    return render_template('create_quiz.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/create_acount', methods=['GET', 'POST'])
def create_acount():
    if request.method == 'POST':
        username = request.form.get('userName')
        email = request.form.get('userEmail')
        password = request.form.get('userPassword')
        name = request.form.get('name', '')
        
        if not username or not email or not password:
            flash('Заполните все поля!', 'error')
            return redirect(url_for('create_acount'))
        
        if user_exists(email, username):
            flash('Пользователь с таким именем или почтой уже существует!', 'error')
            return redirect(url_for('create_acount'))
        
        result = create_user(username, email, password, name)
        if result['success']:
            flash('Регистрация успешна! Теперь войдите в аккаунт.', 'success')
            return redirect(url_for('acount'))
        else:
            flash(result['error'], 'error')
            return redirect(url_for('create_acount'))
    return render_template('create_acount.html')

@app.route('/acount', methods=['GET', 'POST'])
def acount():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('userEmail')
        password = request.form.get('userPassword')
        
        if not email or not password:
            flash('Заполните все поля!', 'error')
            return redirect(url_for('acount'))
        user = check_login(email, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            
            flash(f'Добро пожаловать, {user["username"]}!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверная почта или пароль!', 'error')
            return redirect(url_for('acount'))
    return render_template('acount.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')