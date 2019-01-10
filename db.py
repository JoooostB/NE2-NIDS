import mysql.connector

host="localhost"
user="root"
passwd="appelflap"
database="ne2-nids"

# Inserting data to the database should follow the following structure:
#
# INSERT INTO `sniffer`
# (`id`, `time`, `src_mac`, `dest_mac`, `protocol`, `version`, `header_length`, `ttl`, `ip_protocol`,
# `src_ip`, `dest_ip`, `udp_src_port`, `udp_dest_port`, `udp_length`, `data`) VALUES (NULL, current_timestamp(),
# 'FC:EC:DA:03:B7:85', '01:00:5E:00:00:FB', '8', '4', '20', '1', '17', '192.168.1.1', '224.0.0.251', '5353',
# '5353', '39552', '');
#


class DB(object):
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

    def query(self, query):
        return self.cursor.execute(query)

    def clear(self):
        return self.cursor.execute('TRUNCATE TABLE sniffer')

    def __del__(self):  # When object goes out of scope, close connection.
        self.conn.close()


db = DB()
