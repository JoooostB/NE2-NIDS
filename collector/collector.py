import datetime

from flask import Flask, request, jsonify
from flask import render_template
from models import Database

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def status():
    if request.method == 'GET':
        print("get all packets from db")

        dbHandler = Database()
        all_packets = dbHandler.list_packets()
        print("all packets from db are = ", all_packets)

        now = datetime.datetime.now().replace(microsecond=0)

        filter_settings = request.form

        print("Filter settings are = ", filter_settings)

        return render_template('index.html', all_packets=all_packets, now=now.isoformat())

    if request.method == 'POST':
        filter_settings = request.form

        if filter_settings['start_time']:
            filter_start_time = filter_settings['start_time']
            print("filter start_time = ", filter_start_time)
        else:
            print("filter start_time = empty")
            filter_start_time = "*"

        if filter_settings['end_time']:
            filter_end_time = filter_settings['end_time']
            print("filter end_time = ", filter_end_time)
        else:
            print("filter end_time = empty = ")
            filter_end_time = datetime.datetime.utcnow().replace(microsecond=0)

        filter_protocol = []
        if 'protocol_tcp' in filter_settings:
            filter_protocol.append("TCP")
            print("filter_protocol = ", filter_protocol)
        else:
            print("filter_protocol_tcp is empty")

        if 'protocol_udp' in filter_settings:
            filter_protocol.append("UDP")
            print("filter_protocol = ", filter_protocol)
        else:
            print("filter_protocol_udp is empty")

        if 'protocol_icmp' in filter_settings:
            filter_protocol.append("ICMP")
            print("filter_protocol = ", filter_protocol)
        else:
            print("filter_protocol_icmp is empty")

        if len(filter_protocol) != 0:
            filter_protocol = '|'.join(filter_protocol)
        else:
            filter_protocol = "TCP|UDP|ICMP"
        print("protocol is", filter_protocol)
        print("start time is", filter_start_time)
        print("end time is", filter_end_time)

        dbHandler = Database()
        filter_result = dbHandler.filter_db(filter_protocol, filter_start_time, filter_end_time)

        print("print result = ", filter_result)

        all_packets = dbHandler.list_packets()
        print("all packets from db are = ", all_packets)

        now = datetime.datetime.now().replace(microsecond=0)
        print("now is het volgende ")

        filter_settings = request.form

        print("Filter settings are = ", filter_settings)

        return render_template('index.html', all_packets=all_packets, now=now.isoformat(), filter_result=filter_result)


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
