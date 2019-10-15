from flask import Flask, render_template, redirect, flash, url_for, request
from formF import InputForm
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_script import Manager

try:
	connection = psycopg2.connect(user="postgres",
								password="zarlynx",
								host="127.0.0.1",
								port="5432",
								database="flask_app_db")

	cursor = connection.cursor()
	# Print PostgreSQL Connection properties
	print(connection.get_dsn_parameters(), "\n")

	# Print PostgreSQL version
	cursor.execute("SELECT version();")
	record = cursor.fetchone()
	print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL", error)
finally:
	# closing database connection.
	if (connection):
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")

app = Flask(__name__)
manager = Manager(app)
app.debug = True
app.config['SECRET_KEY'] = 'Sneaky lynx hides in the bushes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:zarlynx@localhost/flask_app_db'

db = SQLAlchemy(app)


@app.route('/')
def index_redirect():
	return redirect(url_for('input_page'))


@app.route('/input_name/', methods=['get', 'post'])
def input_page():
	form = InputForm()
	if form.validate_on_submit():
		name = form.name.data
		print(name)

		feedback = Saver(name=name)
		db.session.add(feedback)
		db.session.commit()

		print("\nData received. Now redirecting ...")
		flash('Name was submitted successfully', "success")
		return redirect(url_for('input_page'))

	return render_template('input.html', form=form)


class Saver(db.Model):
	__tablename__ = 'saved_names'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(1000), nullable=False)

	def __repr__(self):
		return "<{}:{}>".format(id, self.name)


if __name__ == "__main__":
	manager.run()
