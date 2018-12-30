from flask import Flask, render_template, url_for

app = Flask(__name__)

def test():
    print("TEst tsetsets")

@app.route('/')
def dashboard():
    user = {'username': 'Sander'}
    return render_template('index.html', title='Home', user=user)