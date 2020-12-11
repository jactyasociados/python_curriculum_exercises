from flask import Flask, render_template, request # we are now importing just more than Flask!

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/person/<name>/<int:age>')
def person(name, age):
    return render_template('person.html', name = name, age = age)

# we need a route to render the form
@app.route('/calculate')
def show_calc():
    return render_template('calc.html')

# we need to do something when the form is submitted
@app.route('/math')
def calculus():
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    calc = request.args.get('calculation')
    if calc == 'add':
        return str(int(num1) + int(num2))
    if calc == 'sub':
        return str(int(num1) - int(num2))
    if calc == 'mul':
        return str(int(num1) * int(num2))
    if calc == 'div':
        return str(int(num1) / int(num2))
    else:
        return "Invalid Operation"
    
    
if __name__ == '__main__':
    app.run(debug=True)
