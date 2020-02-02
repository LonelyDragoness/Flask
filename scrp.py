from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from forms import ContactForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_script import Manager
import psycopg2


try:
    connection = psycopg2.connect(user="postgres",
                                  password="zarlynx",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="flask_app_db")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


app = Flask(__name__)
manager = Manager(app)
app.debug = True
app.config['SECRET_KEY'] = 'Lynx is a beautiful and quiet animal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:zarlynx@localhost/flask_app_db'

db = SQLAlchemy(app)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login/', methods=['post', 'get'])
def login():
	message = ''
	username = ''
	password = ''

	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

	if username == 'root' and password == 'pass':
		message = "Correct username and password"
	else:
		message = "Wrong username or password"

	return render_template('login.html', message=message)


@app.route('/contact/', methods=['get', 'post'])
def contact():
	form = ContactForm()
	if form.validate_on_submit():
		name = form.name.data
		email = form.email.data
		message = form.message.data
		print(name)
		print(Post)
		print(email)
		print(message)

		feedback = Feedback(name=name, email=email, message=message)
		db.session.add(feedback)
		db.session.commit()

		print("\nData received. Now redirecting ...")
		flash('Message was sent successfully', "success")
		return redirect(url_for('contact'))

	return render_template('contact.html', form=form)


@app.route('/cookie/')
def cookie():
	if not request.cookies.get('1cookie1'):
		res = make_response("Setting a cookie")
		res.set_cookie('1cookie', 'BeautifulLynx', max_age=60*60*24*365*2)
	else:
		res = make_response("Value of cookie 1cookie1 is {}".format(request.cookies.get('1cookie1')))
	return res


@app.route('/visits-counter/')
def visits():
	if 'visits' in session:
		session['visits'] = session.get('visits') + 1
	else:
		session['visits'] = 1
	return "Total visits: {}".format(session.get('visits'))


@app.route('/update-session/')
def updating_session():
	res = str(session.items())

	cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
	if 'cart_item' in session:
		session['cart_item']['pineapples'] = '100'
		session.modified = True
	else:
		session['cart_item'] = cart_item

	return res


@app.route('/delete-visits/')
def delete_visits():
	session.pop('visits', None)
	return "Visits deleted..."


class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	slug = db.Column(db.String(255), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)
	posts = db.relationship('Post', backref='category')

	def __repr__(self):
		return "<{}:{}>".format(id, self.name)


post_tags = db.Table('post_tags',
	db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	slug = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text(), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)
	updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
	category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

	def __repr__(self):
		return "<{}:{}>".format(self.id,  self.title[:10])


class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	slug = db.Column(db.String(255), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)
	posts = db.relationship('Post', secondary=post_tags, backref='tags')


class Feedback(db.Model):
	__tablename__ = 'feedbacks'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(1000), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	message = db.Column(db.Text(), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return "<{}:{}>".format(id, self.name)


if __name__ == "__main__":
	manager.run()
def flag(N):
	class ArgumentError(Exception):
		pass

	if not isinstance(N, int) or N % 2 != 0 or N <= 0:
		raise ArgumentError("N should be an integer even number")

	# Creating the lines before the circle
	output_string = ('#' * (N * 3 + 2) + '\n')
	for i in range(int(N / 2)):
		output_string += ('#' + ' ' * (N * 3) + '#\n')

	# Creating first half of the circle
	for i in range(0, N, 2):
		output_string += ('#' + ('*' + 'o' * i + '*').center(3 * N, ' ') + '#\n')

	# Second half of the circle and the lines are mirrored
	output_string += output_string[-2::-1]

	return output_string