from flask import Flask, escape, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    todo = Todo(title=title,complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)