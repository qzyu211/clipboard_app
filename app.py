from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy, event
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Clipboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@event.listens_for(Clipboard.__table__, 'after_create')
def create_clipboard_items(*args, **kwargs):
    db.session.add(Clipboard(item_name='Name', content='Your name'))
    db.session.add(Clipboard(item_name='Email', content='email@address.com'))
    db.session.add(Clipboard(item_name='Address', content='123 Blvd.'))
    db.session.add(Clipboard(item_name='LinkedIn', content='https://www.linkedin.com/in/your-li-name/'))
    db.session.add(Clipboard(item_name='GitHub Page', content='https://your-github-page.github.io'))
    db.session.commit()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item_name = request.form['item_name']
        task_content = request.form['content']
        new_task = Clipboard(item_name=item_name, content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Clipboard.query.order_by(Clipboard.item_name).all()
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