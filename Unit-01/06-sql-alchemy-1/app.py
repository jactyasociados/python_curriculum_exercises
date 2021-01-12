from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1to1anyherzt@127.0.0.1:5432/flask-snacks-app'
modus = Modus(app)
db = SQLAlchemy(app)

class Snack(db.Model):
	__tablename__ = "snacks"
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	kind = db.Column(db.Text)
	
	def __init__(self, name, kind):
		self.name = name
		self.kind = kind

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/snacks', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
    	new_snack = Snack(request.form['name'], request.form['kind'])
    	db.session.add(new_snack)
    	db.session.commit()
    	return redirect(url_for('index'))
    return render_template('index.html', snacks=Snack.query.all())

@app.route('/snacks/new')
def new():
    return render_template('new.html')

@app.route('/snacks/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    try: 
        # Refactored using a generator so that we do not need to do [0]!
        found_snack = Snack.query.get(id)
    except:
    	return render_template('404.html')

    # if we are updating a toy...
    if request.method == b"PATCH":
        found_snack.name = request.form['name']
        found_snack.kind = request.form['kind']
        db.session.add(found_snack)
        db.session.commit()
        return redirect(url_for('index'))
        
    if request.method == b"DELETE":
        db.session.delete(found_snack)
        db.session.commit()
        return redirect(url_for('index'))
    
    # if we are showing information about a snack
    return render_template('show.html', snack=found_snack)

@app.route('/snacks/<int:id>/edit')
def edit(id):
    try:
        # Refactored using a generator so that we do not need to do [0]!
        found_snack = Snack.query.get(id)
        return render_template('edit.html', snack=found_snack)
    except:
       return render_template('404.html')    
       
if __name__ == '__main__':
    app.run(debug=True, port=5000)