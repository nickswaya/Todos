from os import environ # this line should go at the top of your file

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user

FLASK_APP = Flask(__name__)
FLASK_APP.config['SECRET_KEY'] = 'mysecret'
FLASK_APP.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
FLASK_APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(FLASK_APP)
db.create_all()



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
   return redirect('/')

@FLASK_APP.route('/', methods= ['GET','POST'])
def index():
    if 'todo' in request.form:
        db.session.add(Todo(todo_text = request.form['todo']))
        db.session.commit()
        return redirect('/')
    return render_template('index.html', todos=Todo.query.all(), template_form = TodoForm()) 

@FLASK_APP.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    
    db.session.add(User(username=form.username.data, email=form.email.data))
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

@FLASK_APP.route('/userlist', methods=['GET', 'POST'])
def UserList():
    current_users = User.query.all()
    return render_template('userlist.html', current_users = current_users)