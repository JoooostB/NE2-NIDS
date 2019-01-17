import mysql.connector


class Database:
    def __init__(self):

        self.con = mysql.connector.connect(user='ne2_admin',
                                           password='appelflap',
                                           host='db',
                                           database='collector')
        self.cur = self.con.cursor()

    def list_packets(self):
        self.cur.execute("SELECT protocol, src_address, bytes, packets, date FROM collector")
        result = self.cur.fetchall()
        self.con.close()

        return result

