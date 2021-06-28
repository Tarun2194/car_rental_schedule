from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.model):
    id = db.column(db.Integer, primary_key=True)
    content = db.column(db.String(1000), nullable=False)
    completed = db.column(db.Integer, default=0)
    date_created = db.column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Sorry, task not added'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('template.html', tasks=tasks)


@app.route('/delete/<int:id')
def delete(id):
    task_to_delete = Todo.guery.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return ' Problem identified '


@app.route('/upadte/<int:id', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'sorry , update action not done'

    else:
        return render_template('update.html', task=task)


# Press the green button in the gutter  to run the script.
if __name__ == '__main__':
    app.run(debug=True)
