import mysql.connector

host = "db"
user = "root"
passwd = "appelflap"
database = "collector"


class Database(object):
    """This class is responsible for setting up a connection to the database and executing simple queries."""
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            if self.conn:
                self.cursor = self.conn.cursor()
                print('Success')
        except mysql.connector.Error as err:
            if err == 1049:
                print('Unknown database: ' + database)
            else:
                print(err)

    def list_packets(self):
        self.cursor.execute("SELECT protocol, src_address, bytes, packets, date FROM collector")
        result = self.cursor.fetchall()
        return result

    def insert_packet(self, packet_protocol, packet_ip, packet_bytes):
        print("inserting packet in db")
        self.cursor.execute("INSERT INTO collector (protocol, src_address, bytes) VALUES (%s, %s, %s)",
                         (packet_protocol, packet_ip, packet_bytes))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
