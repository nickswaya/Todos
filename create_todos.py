from app import db, Todo
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
engine = create_engine('sqlite:///myDB.db', echo = True)
from app import db

meta = MetaData()
users = Table(
   'users', meta, 
   Column('id', Integer, primary_key = True), 
   Column('username', String), 
   Column('password', String),
   Column('email', String) 
)
db.create_all()
meta.create_all(engine)


print('x')

db.create_all()
first_todo = Todo(todo_text= "Learn Flask")
a = Todo(todo_text= "Rocket League")
s = Todo(todo_text= "Get money")
db.session.add(first_todo)
db.session.add(a)
db.session.add(s)
db.session.commit()