from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome!"
    
@app.route('/math/<calculation>/<int:num1>/<int:num2>')
def calculator(calculation, num1, num2):
    if calculation == 'add':
        return str(num1 + num2)
    elif calculation == 'sub':
        return str(num1 - num2)
    elif calculation == 'mul':
        return str(num1 * num2)
    elif calculation == 'div':
        return str(num1 / num2)
    else:
        return "Invalid Operation"
