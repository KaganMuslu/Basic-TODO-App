from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
URI = os.getenv('URI')
app.config["SQLALCHEMY_DATABASE_URI"] = URI

app.app_context().push()
db = SQLAlchemy(app)
 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    complate = db.Column(db.Boolean)



@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.id.asc()).all()

    return render_template('index.html', todos = todos)

@app.route('/add', methods=['POST'])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")

    newTodo = Todo(title=title, content=content, complate=False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complate/<string:id>')
def complateTodo(id):
    query = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    if query.complate == True:
        query.complate = False
    else:
        query.complate = True
        
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def deleteTodo(id):
    query = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    db.session.delete(query)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/detail/<string:id>')
def detailTodo(id):
    query = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    
    
    return render_template('detail.html', todo=query)

if __name__ == '__main__':
    app.run(debug=True)