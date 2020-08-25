from os import environ # this line should go at the top of your file

from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

FLASK_APP = Flask(__name__)
FLASK_APP.config['SECRET_KEY'] = 'mysecret'
FLASK_APP.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
FLASK_APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(FLASK_APP)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_text = db.Column(db.String(100), index = True)

class TodoForm(FlaskForm):
    todo= StringField('Todo', validators=[DataRequired()])
    submit = SubmitField('Add Todo')



@FLASK_APP.route('/', methods= ['GET', 'POST'])

def index():
    if 'todo' in request.form:
        db.session.add(Todo(todo_text = request.form['todo']))
        db.session.commit()
        return redirect('/')
    return render_template('index.html', todos=Todo.query.all(), template_form = TodoForm()) 



