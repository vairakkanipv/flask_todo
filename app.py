from flask import Flask, flash, escape, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'V@iRaKk@Ni'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

db.create_all()
db.session.commit()


@app.route('/hello')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/')
def index():
    # db.create_all()
    # db.session.commit()
    # my_dodo_list = Todo.query.all()
    # print(my_dodo_list)
    # todo = Todo(title='My_doo1',complete=False)
    # db.session.add(todo)
    # db.session.commit()
    not_complete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html',not_complete=not_complete,complete=complete)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title'].strip()
    if title :
        todo = Todo(title=title,complete=False)
        db.session.add(todo)
        db.session.commit()
        flash('You were successfully added into todo list','success')
    else:
        flash('Failed invalid input','error')
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/not_complete/<id>')
def not_complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    return render_template('edit.html',todo=todo)

@app.route('/update',methods=['POST'])
def update():
    id = request.form['id']
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.title = request.form['title']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    #app.run(debug=True)
    #app.run(host='192.111.222.333', port=4005, debug =True)
    app.run(port=4005, debug =True)