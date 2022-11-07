from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasksdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
Bootstrap(app)




class TaskForm(FlaskForm):
    task_name = StringField('Add a new task....', validators=[DataRequired()])
    due_date = DateField('Add a Due date....', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Tasks(db.Model):
    __tablename__ = "Task_List"
    ID = db.Column(db.Integer, primary_key=True)
    Desc = db.Column(db.String(250), nullable=False)
    Due_Date = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()



@app.route('/', methods = ['GET', 'POST'])
def run():
    form = TaskForm()
    if form.validate_on_submit():
        new_post = Tasks(
        Desc=form.task_name.data,
        Due_Date = form.due_date.data
        )
        db.session.add(new_post)
        db.session.commit()

        return redirect("/")

    now = dt.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    task_list = Tasks.query.order_by(Tasks.Due_Date).all()
    return render_template('index.html', current_time = date_time, form = form, tasks = task_list)



@app.route('/delete/<int:item_id>', methods = ['GET', 'POST'])
def delete(item_id):
    post_to_delete = Tasks.query.get(item_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)
