from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from snack import Snack

app = Flask(__name__)
modus = Modus(app)

snacks = [Snack('banana','fruit')]

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/snacks', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
    	new_snack = Snack(request.form['name'], request.form['kind'])
    	snacks.append(new_snack)
    	return redirect(url_for('index'))
    return render_template('index.html', snacks=snacks)

@app.route('/snacks/new')
def new():
    return render_template('new.html')

@app.route('/snacks/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    try: 
        # Refactored using a generator so that we do not need to do [0]!
        found_snack = next(snack for snack in snacks if snack.id == id)
    except:
    	return render_template('404.html')

    # if we are updating a toy...
    if request.method == b"PATCH":
        found_snack.name = request.form['name']
        found_snack.kind = request.form['kind']
        return redirect(url_for('index'))
        
    if request.method == b"DELETE":
        snacks.remove(found_snack)
        return redirect(url_for('index'))
    
    # if we are showing information about a toy
    return render_template('show.html', snack=found_snack)

@app.route('/snacks/<int:id>/edit')
def edit(id):
    try:
        # Refactored using a generator so that we do not need to do [0]!
        found_snack = next(snack for snack in snacks if snack.id == id)
        return render_template('edit.html', snack=found_snack)
    except:
       return render_template('404.html')    
       
if __name__ == '__main__':
    app.run(debug=True, port=5000)
