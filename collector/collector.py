from flask import Flask, request
from flask import render_template
from models import Database
app = Flask(__name__)

dbHandler = Database()


@app.route('/', methods=['GET'])
def hello():
    if request.method == 'GET':
        print("get all packets from db")
        all_packets = dbHandler.list_packets()
        print("all packets from db are = ", all_packets)
        return render_template('index.html', all_packets=all_packets)


@app.route('/insert_db', methods=['POST'])
def insert_db():
    if request.method == 'POST':
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
