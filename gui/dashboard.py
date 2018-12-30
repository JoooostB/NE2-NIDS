from flask import Flask, render_template
import subprocess

app = Flask(__name__)

def test():
    print("TEst tsetsets")

@app.route('/')
def dashboard():

    def inner():
        proc = subprocess.Popen(
            test(),
            shell=True,
            stdout=subprocess.PIPE
        )

    while proc.poll() is None:
        yield proc.stdout.readline() + '<br/>\n'
    return flask.Response(inner(),
                          mimetype='text/html')  # text/html is required for most browsers to show the partial page immediately

    user = {'username': 'Sander'}
    return render_template('index.html', title='Dashboard sniffer', user=user)

app.run(debug=True, port=5000)
