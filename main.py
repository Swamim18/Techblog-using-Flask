from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '4191628bb0b13ce2c676dfde946ba369'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# isAuthenticated, isActive, isAnnonymous, getID Required attributes
login_manager = LoginManager(app)


@login_manager.user_loader  # decorator for login manager
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db. Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'Swamim Saikia',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'February 03, 2019'
    },
    {
        'author': 'Nikhil Patil',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'February 04, 2019'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        '''hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')'''
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # f works on python 3.6 and ablove only
        flash('Your account is created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:

            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
