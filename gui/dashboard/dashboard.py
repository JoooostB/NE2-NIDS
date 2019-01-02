from flask import Flask, render_template, url_for
import flask
from sniffer.sniffer import sniffer

app = Flask(__name__)

@app.route('/')
def dashboard():
    return flask.Response(sniffer(), mimetype='text/html')