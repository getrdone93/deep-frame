#Server Connection to MySQL:

import MySQLdb
import os

def connect():
    conn = MySQLdb.connect(host=os.environ['DB_HOST'],
                      user=os.environ['DB_USER'],
                      passwd=os.environ['DB_PASS'],
                      db="engy1")
    x = conn.cursor()
    try:
       x.execute("""INSERT INTO anooog1 VALUES (%s,%s)""",(188,90))
       conn.commit()
    except:
       conn.rollback()

    conn.close()

if __name__ == '__main__':
    connect()
