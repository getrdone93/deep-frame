import mysql.connector as msc
import os
import traceback

def connect():
    conn = None
    try:
        conn = msc.connect(host=os.environ['DB_HOST'],
                           port=int(os.environ['DB_PORT']),
                           user=os.environ['DB_USER'],
                           passwd=os.environ['DB_PASS'],
                           db=os.environ['DB_DATABASE'])
        cursor = conn.cursor()
        insert = "insert into deep_learning (name) values (%s)" 
        for i in range(5):
            values = ("Approach: " + str(i),)            
            cursor.execute(insert, values)
            conn.commit()
            print("Inserted value " + values[0])
    except BaseException as e:
        traceback.print_exc()
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    

if __name__ == '__main__':
    connect()
