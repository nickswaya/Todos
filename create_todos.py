from app import db, Todo
db.create_all()


print('x')


first_todo = Todo(todo_text= "Learn Flask")
a = Todo(todo_text= "Rocket League")
s = Todo(todo_text= "Get money")
db.session.add(first_todo)
db.session.add(a)
db.session.add(s)
db.session.commit()