from flask import Flask, request, jsonify
from flask import render_template
from models import Database

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    if request.method == 'GET':
        print("get all packets from db")

        dbHandler = Database()
        all_packets = dbHandler.list_packets()

        print("all packets from db are = ", all_packets)

        return render_template('index.html', all_packets=all_packets)


@app.route('/insert_packet', methods=['POST'])
def insert_db():
    if request.method == 'POST':

        packet = request.get_json(force=True)

        print("packet is = ", packet)

        packet_ip = packet['packet']['ip']
        packet_protocol = packet['packet']['protocol']
        packet_bytes = packet['packet']['bytes']

        print("packet ip is = ", packet_ip)
        print("packet protocol is = ", packet_protocol)
        print("packet bytes is = ", packet_bytes)

        dbHandler = Database()
        dbHandler.insert_packet(packet_protocol, packet_ip, packet_bytes)

        dict_to_return = {"Status": "packet inserted"}

        return jsonify(dict_to_return)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
