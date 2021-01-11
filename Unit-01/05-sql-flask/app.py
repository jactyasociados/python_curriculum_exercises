from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
import db

app = Flask(__name__)
modus = Modus(app)

db.create_table()

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/snacks', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
    	db.create_snack(request.form['name'], request.form['kind'])
    	return redirect(url_for('index'))
    return render_template('index.html', snacks=db.find_all_snacks())

@app.route('/snacks/new')
def new():
    return render_template('new.html')

@app.route('/snacks/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    
    
    
    if request.method == b"PATCH":
        snack_name = request.form['name']
        snack_kind = request.form['kind']
        db.edit_snack(snack_name, snack_kind, id)
        return render_template('index.html', snacks=db.find_all_snacks())
    
    elif request.method == b"DELETE":
        db.remove_snack(id)
        return render_template('delete.html')
    elif not(request.method == b"PATCH" or request.method == b"DELETE"):
        return render_template('show.html', snacks=db.find_snack(id))
    
    

@app.route('/snacks/<int:id>/edit')
def edit(id):
    snacks = db.find_snack(id)
    #found_toy = next( toy for toy in  toys if toy.id == id)
    return render_template('edit.html', snacks=snacks)
       
if __name__ == '__main__':
    app.run(debug=True, port=5000)