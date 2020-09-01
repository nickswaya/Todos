from os import environ # this line should go at the top of your file

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user

FLASK_APP = Flask(__name__)
FLASK_APP.config['SECRET_KEY'] = 'mysecret'
FLASK_APP.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
FLASK_APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(FLASK_APP)
db.create_all()
login_manager = LoginManager()
login_manager.init_app(FLASK_APP)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_text = db.Column(db.String(100), index = True)
    
class TodoForm(FlaskForm):
    todo= StringField('Todo', validators=[DataRequired()])
    submit = SubmitField('Add Todo')


@FLASK_APP.route('/remove_item/<id>', methods= ['GET','POST'])
def remove_item(id):
   #from the Item model, fetch the item with primary key item_id to be deleted
   db.session.delete(Todo.query.get(id))
   #using db.session delete the item
   #commit the deletion
   db.session.commit()
   flash(message='ToDo Removed!')

   return redirect('/')

@FLASK_APP.route('/', methods= ['GET','POST'])
def index():
    if 'todo' in request.form:
        db.session.add(Todo(todo_text = request.form['todo']))
        db.session.commit()
        if current_user.is_authenticated:
            flash(message='Todo Created! Thank you {}.'.format(current_user.username))
            return redirect('/')
        if not current_user.is_authenticated:
            flash(message='Todo Created! Thank you anonymous user.')
            return redirect('/')
    return render_template('index.html', todos=Todo.query.all(), template_form = TodoForm(), form=LoginForm()) 

@FLASK_APP.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
  return render_template('register.html', form=form)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)    


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')
  

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


@FLASK_APP.route('/userlist', methods=['GET', 'POST'])
@login_required
def UserList():
    current_users = User.query.all()
    return render_template('userlist.html', current_users = current_users)


@FLASK_APP.route('/login', methods=['GET','POST'])
def login():  
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_password(form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('index'))
    else:
      return redirect(url_for('login', form=form))
  return render_template('login.html', form=form)    

@FLASK_APP.route("/logout")
def logout():
    logout_user()
    return redirect('/')

