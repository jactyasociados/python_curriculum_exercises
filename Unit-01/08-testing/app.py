from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')

#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1to1anyherzt@127.0.0.1:5432/users-messages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

modus = Modus(app)
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	image_url = db.Column(db.Text)
	messages = db.relationship('Message', backref="user", lazy="dynamic", cascade="all, delete")
	emails = db.relationship('Email', backref="person", lazy="dynamic", cascade="all, delete")
	
	def __init__(self, first_name, last_name, image_url):
		self.first_name = first_name
		self.last_name = last_name
		self.image_url = image_url
		
class Message(db.Model):
	__tablename__ = "messages"
	
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	def __init__(self, content, user_id):
		self.content = content
		self.user_id = user_id
		
class Email(db.Model):
    __tablename__ ="emails"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, email, person_id):
    	self.email = email
    	self.person_id = person_id
    
@app.route('/')
def root():
	return redirect(url_for('index'))
	
@app.route('/users', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		new_user = User(request.form['first_name'], request.form['last_name'], request.form['image_url'])
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('users/index.html', users=User.query.all())	
	
@app.route('/users/new')
def new():
	return render_template('users/new.html')
	
@app.route('/users/<int:id>/edit')
def edit(id):
	try:
		found_user = User.query.get(id)
	except:
		render_template('users/404.html')
	
	return render_template('users/edit.html', user=found_user)
	
@app.route('/users/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
	try:
		found_user = User.query.get(id)
	except:
		render_template('users/404.html')
	
	if request.method == b"PATCH":
		found_user.first_name = request.form['first_name']
		found_user.last_name = request.form['last_name']
		db.session.add(found_user)
		db.session.commit()
		return redirect(url_for('index'))
	
	if request.method == b"DELETE":
		db.session.delete(found_user)
		db.session.commit()
		return redirect(url_for('index'))
	
	
	return render_template('users/show.html', user=found_user)
	
@app.route('/users/<int:user_id>/messages', methods=["GET", "POST"])
def messages_index(user_id):
	if request.method == "POST":
		new_message=Message(request.form['content'], user_id)
		db.session.add(new_message)
		db.session.commit()
		return redirect(url_for('messages_index', user_id=user_id))
	return render_template('messages/index.html', user=User.query.get(user_id))
	
@app.route('/users/<int:user_id>/messages/new', methods=["GET", "POST"])
def messages_new(user_id):
	return render_template('messages/new.html', user=User.query.get(user_id))
	
@app.route('/users/<int:user_id>/messages/<int:id>/', methods=["GET","POST"])
def messages_edit(user_id, id):
	found_message = Message.query.get(id)
	return render_template('messages/edit.html', message=found_message)
	
@app.route('/users/<int:user_id>/messages_show/<int:id>/', methods=["GET", "PATCH", "DELETE"])
def messages_show(user_id, id):
	found_message = Message.query.get(id)
	
	if request.method == b"PATCH":
		found_message.content = request.form['content']
		db.session.add(found_message)
		db.session.commit()
		return redirect(url_for('messages_index', user_id=user_id))
	
	if request.method == b"DELETE":
		db.session.delete(found_message)
		db.session.commit()
		return redirect(url_for('messages_index', user_id=user_id))
	
	return render_template('messages_show/show.html', message=found_message)
	    
#emails urls

@app.route('/users/<int:person_id>/emails', methods=["GET", "POST"])
def emails_index(person_id):
	if request.method == "POST":
		new_email=Email(request.form['email'], person_id)
		db.session.add(new_email)
		db.session.commit()
		return redirect(url_for('emails_index', person_id=person_id))
	return render_template('emails/index.html', person=User.query.get(person_id))
	
@app.route('/users/<int:person_id>/emails/new', methods=["GET", "POST"])
def emails_new(person_id):
	return render_template('emails/new.html', person=User.query.get(person_id))
	
@app.route('/users/<int:person_id>/emails/<int:id>/', methods=["GET", "POST"])
def emails_edit(person_id, id):
	found_email = Email.query.get(id)
	return render_template('emails/edit.html', email=found_email)
	
@app.route('/users/<int:person_id>/emails_show/<int:id>/', methods=["GET", "PATCH", "DELETE"])
def emails_show(person_id, id):
	found_email = Email.query.get(id)
	
	if request.method == b"PATCH":
		found_email.email = request.form['email']
		db.session.add(found_email)
		db.session.commit()
		return redirect(url_for('emails_index', person_id=person_id))
	
	if request.method == b"DELETE":
		db.session.delete(found_email)
		db.session.commit()
		return redirect(url_for('emails_index', person_id=person_id))
	
	return render_template('emails_show/show.html', email=found_email)
		
if __name__ == '__main__':
	app.run(debug=True)
