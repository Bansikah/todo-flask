from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#db.init_app(app)

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def addTodo():
    name = request.form.get('name')
    newTodo = Todo(name=name, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('home'))

##update function
@app.route('/update/<int:id>')
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
 with app.app_context():
    db.create_all()
    app.run(debug=True)