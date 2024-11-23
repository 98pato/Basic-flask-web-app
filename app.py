from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
db = SQLAlchemy(app)

# Define the database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    content = db.Column(db.String(200), nullable=False)  # Task content, cannot be empty
    completed = db.Column(db.Integer, default=0)  # Default completion status is 0 (not completed)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically add creation date

    def __repr__(self):
        return f'<Task {self.id}>'

# Route for the homepage
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
            return 'There was an issue adding your task'


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


# Entry point for the application
if __name__ == "__main__":
    # Create the database and table(s) if they don't already exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)


