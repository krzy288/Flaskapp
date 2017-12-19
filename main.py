from flask import Flask, render_template, redirect, url_for, sessions,logging, request, flash
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField,TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

Articles = Articles()

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'password'
app.config["MYSQL_DB"] = 'myflaskapp'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'


mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route("/article/<string:id>")
def article(id):
    return render_template('article.html', id=id)




class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1,max=50)])
    username =StringField("Username", [validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=6,max=12)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.EqualTo('confirm', message='Password not match')
    ])
    confirm = PasswordField('Confirm password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        mysql.connect
        print("DB connection ok")
    except Exception as e:
        print(str(e))


    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #cursor
        cur = mysql.connection.cursor()

        cur.execute( "Insert into users(name,email,username,password) values(%s,%s,%s,%s)" , (name,email,username,password))
        mysql.connection.commit()
        cur.close()

        flash("User registered correctly", 'success')



        return render_template('register.html', form=form)
    return render_template('register.html',form=form)

if __name__=='__main__':
    app.secret_key='1234567'
    app.run(debug=True)



