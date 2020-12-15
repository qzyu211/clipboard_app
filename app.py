from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy, event
from datetime import datetime
import os
from config import setup_dic

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

class Clipboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.REAL, default=0, nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@event.listens_for(Clipboard.__table__, 'after_create')
def create_clipboard_items(*args, **kwargs):
    for index, (key, value) in enumerate(setup_dic.items()):
        db.session.add(Clipboard(item_name=key, order_id=index, content=setup_dic[key]))
    db.session.commit()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        order_id = request.form['order_id']
        item_name = request.form['item_name']
        task_content = request.form['content']
        new_task = Clipboard(order_id=order_id, item_name=item_name, content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Clipboard.query.order_by(Clipboard.order_id).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Clipboard.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Clipboard.query.get_or_404(id)

    if request.method == 'POST':
        task.order_id = request.form['order_id']
        task.item_name = request.form['item_name']
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)