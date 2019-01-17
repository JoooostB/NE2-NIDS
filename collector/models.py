import mysql.connector
host = "db"
user = "ne2-nids"
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
        result = self.cur.fetchall()
        self.conn.close()
        return result

    def clear(self):
        return self.cursor.execute('TRUNCATE TABLE collector')

    def __del__(self):  # When object goes out of scope, close connection.
        self.conn.commit()
        self.conn.close()

