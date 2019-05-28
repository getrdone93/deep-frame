import tensorflow as tf
import pprint
import db_conn
from absl import flags

flags.DEFINE_string('event_file_path', None, 'Path to event file to insert into database')

def read_event_file(pp, db, base_query, file_name=None, types=(float, bytes)):
    if file_name is None:
        tf.logging.info("file_name was none, doing nothing")
    else:
        for ev in tf.train.summary_iterator(file_name):
            out = {}
            out['step'] = ev.step
            out['wall_time'] = ev.wall_time
            tag_val = {}
            for v in ev.summary.value:
                try:
                    tag_val[v.tag] = v.simple_value
                except AttributeError:
                    tf.logging.info("ERROR: could not get %s from: %s" % ("simple_value", v.tag))

            if out['learning_rate'] is None:
                continue
            query = base_query % (out['learning_rate'])          
            db.insert(query, (1, 1, out['learning_rate']))

if __name__ == '__main__':
    database = db_conn.Database()
    database.open_connection()
    pp = pprint.PrettyPrinter(indent=4)
    read_event_file(pp, database, db_conn.QUERY, flags.EVENT_FILE_PATH)
    database.close_connection()


