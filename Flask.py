from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_session import Session
import os

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=0, max=50)])
    username = StringField('Username', [validators.Length(min=0, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=0, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config[''] = 1800
PERMANENT_SESSION_LIFETIME = 1800
#yukarıdaki kod neden çalıştı bilmiyorum
app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flask"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mySQL = MySQL(app)


@app.route('/Register', methods=['GET', 'POST'])
def register():

        if request.method == 'POST':
            form = RegisterForm(request.form)
            name = form.name.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))
            cursor = mySQL.connection.cursor()
            query = "INSERT INTO users(name,username,password) VALUES(%s,%s,%s)"
            cursor.execute(query, (name, username, password))
            mySQL.connection.commit()
            cursor.close()
            flash("You are now registered and can log in", "success")
            return redirect(url_for('login'))
        else:
            form = RegisterForm(request.form)
            return render_template('register.html', form=form)


@app.route('/Maclaren')
def dashboard():
    return render_template('Maclaren.html')
@app.route('/New')
def new():
        cursor = mySQL.connection.cursor()
        query = "SELECT * FROM users " 
        result = cursor.execute(query)
        print(cursor.fetchone())
        return render_template('New.html',{'query': cursor.fetchall()})
    
@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password_entered = form.password.data
        cursor = mySQL.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s" 
        result = cursor.execute(query, (username,))
 
        if result > 0:
            data = cursor.fetchone()
            if sha256_crypt.verify(password_entered,data["Password"]):
                flash("You are logged in", "success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Password is not correct", "danger")
                return redirect(url_for("login"))
        else:
            flash("Username not found", "danger")
            return redirect(url_for("login"))
    return render_template('login.html',form=form)


@app.route('/Logout')
def logout():
    session.clear()
    flash("You are logged out", "success")
    return redirect(url_for("index"))






















@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/About')
def about():
    return render_template('About.html')


"""
    {"id":1,"title","a","content",b}
    {"id":2,"title","a","content",b}
    {"id":3,"title","a","content",b}
"""


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True, threaded=True)