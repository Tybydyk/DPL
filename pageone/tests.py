import pymysql
from DPL.settings import MYSQL_KEY

def check_connection(connection):
    assert connection.host_info == 'socket localhost:3306'


if __name__ == "__main__":
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password=MYSQL_KEY,
                                 database='dbTest')


    check_connection(connection)
