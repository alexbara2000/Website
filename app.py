import csv
import os
import datetime
from flask import Flask, render_template, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required
from forms import SignUpForm, LoginForm, ForgotPassword

app = Flask(__name__)
app.secret_key = 'qwx3453y4g6g53f5676564f424565'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username):
        self.id = username


def replace_password(username, password):
    with open('data/passwords.csv', 'r') as y:
        reader = csv.reader(y)

        with open('data/temp.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for user in reader:
                if username == user[0]:
                    writer.writerow([username, password])
                else:
                    writer.writerow([user[0], user[1]])
    os.remove('data/passwords.csv')

    with open('data/temp.csv', 'r') as y:
        reader = csv.reader(y)

        with open('data/passwords.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for user in reader:
                writer.writerow([user[0], user[1]])
    os.remove('data/temp.csv')


def login_list(username, x):
    time = datetime.datetime.now()
    with open('data/logins.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([time, username, x])


def find_user(username):
    with open('data/passwords.csv') as f:
        for user in csv.reader(f):
            if username == user[0]:
                return user[0]
    return 'na'


def check_password(username, password):
    with open('data/passwords.csv') as f:
        for user in csv.reader(f):
            if username == user[0] and password == user[1]:
                return True
    return False


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def default():
    return render_template('front-page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        if check_password(name, password):
            login_list(name, 'Login')
            login_user(User(name))
            session['username'] = name
            return redirect('/home')
            next_page = session.get('next', '/home')
            session['next'] = '/home'
            return redirect(next_page)
        else:
            flash("Incorrect username or password. If you do not have an account, please press signup")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    login_list(session['username'], 'Logout')
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = find_user(username)
        if user == 'na':
            with open('data/passwords.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, password])
            return redirect('/login')
        else:
            flash('This username already exists, choose another one')
    return render_template('signup.html', form=form)


@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotpass():
    form = ForgotPassword()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = find_user(username)
        if user != 'na' and user != 'admin':
            replace_password(username, password)
            return redirect('/login')
        else:
            flash('Username not found')
    return render_template('forgot-password.html', form=form)


@app.route('/home')
@login_required
def home():
    login_list(session['username'], 'Home')
    return render_template('home.html', username=session.get('username'))


@app.route('/EarlyChildhood')
@login_required
def EarlyChildhood():
    login_list(session['username'], 'EarlyChildhood')
    return render_template('EarlyChildhood.html')


@app.route('/Childhood')
@login_required
def Childhood():
    login_list(session['username'], 'Childhood')
    return render_template('Childhood.html')


@app.route('/Adulthood')
@login_required
def Adulthood():
    login_list(session['username'], 'Adulthood')
    return render_template('Adulthood.html')


@app.route('/statistics')
@login_required
def secret():
    if session['username'] == 'admin':
        login_list(session['username'], 'statistics')
        items =[]
        with open('data/logins.csv', 'r') as f:
            reader = csv.reader(f)
            for user in reader:
                item = dict(date=user[0], name=user[1], place=user[2])
                items.append(item)

        passwords = []
        with open('data/passwords.csv', 'r') as f:
            reader = csv.reader(f)
            for user in reader:
                item = dict(username=user[0], password=user[1])
                passwords.append(item)
        return render_template('statistics.html', items=items, passwords=passwords)
    else:
        return redirect('/home')


@app.route('/quiz', methods=['POST', 'GET'])
@login_required
def quiz():
    return render_template('quiz.html')


if __name__ == '__main__':
    app.run()
