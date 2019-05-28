import mysql.connector as msc
import os
import traceback
import tensorflow as tf 

QUERY = 'insert into model (meta_architecture_id_fk, backbone_id_fk, learning_rate) values (%s)'

class Database():

    def __init__(self, host=os.environ['DB_HOST'], port=int(os.environ['DB_PORT']), user=os.environ['DB_USER'], password=os.environ['DB_PASS'], database=os.environ['DB_DATABASE']):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database    
    
    # def open_connection(self):
    #     conn = None
    #     try:
    #         conn = msc.connect(host=self.host,
    #                            port=int(self.port),
    #                            user=self.user,
    #                            passwd=self.password,
    #                            db=self.database)
    #         cursor = conn.cursor()
    #         insert = "insert into deep_learning (name) values (%s)" 
    #         for i in range(5):
    #             values = ("Approach: " + str(i),)            
    #             cursor.execute(insert, values)
    #             conn.commit()
    #             print("Inserted value " + values[0])
    #     except BaseException as e:
    #         traceback.print_exc()
    #         if conn is not None:
    #             conn.rollback()
    #     finally:
    #         if conn is not None:
    #             conn.close()

    def insert(self, query, values):
        try:
            vals = tuple(values)
            cursor = self.connection.cursor()
            cursor.execute(query, vals)
            self.connection.commit()
        except BaseException as e:
            traceback.print_exc()
            

    def open_connection(self):
        if self.connection is None:
            conn = None
            try:
                conn = msc.connect(host=self.host,
                                   port=int(self.port),
                                   user=self.user,
                                   passwd=self.password,
                                   db=self.database)
                self.connection = conn
            except BaseException:
                tf.logging.error('could not open connection')
                traceback.print_exc()                
        else:
            tf.logging.info('no effect, connection is already open')


    def close_connection(self):
        if self.connection is None:
            tf.logging.info('no effect, connection is already closed')
        else:
            try:
                self.connection.close()
            except BaseException:
                traceback.print_exc()
            finally:
                tf.logging.info('connection has been closed')
                    
# if __name__ == '__main__':
#     connect()
