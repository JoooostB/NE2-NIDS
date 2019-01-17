import mysql.connector
host = "db"
user = "root"
passwd = "appelflap"
database = "collector"


class Database(object):
    """This class is responsible for setting up a connection to the database and executing simple queries."""
    def __init__(self):

      self.con = mysql.connector.connect(user='ne2_admin',
                                           password='appelflap',
                                           host='localhost',
                                           database='collector')
        self.cur = self.con.cursor()

    def list_packets(self):
        self.cur.execute("SELECT protocol, src_address, bytes, packets, date FROM collector")
        result = self.cur.fetchall()
        return result

    def insert_packet(self, packet_protocol, packet_ip, packet_bytes):
        print("inserting packet in db")
        self.cur.execute("INSERT INTO collector (protocol, src_address, bytes) VALUES (%s, %s, %s)",
                         (packet_protocol, packet_ip, packet_bytes))
        self.con.commit()

    def __del__(self):
        self.con.close()