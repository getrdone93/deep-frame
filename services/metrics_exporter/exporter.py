import tensorflow as tf
import pprint
import db_lib
from absl import flags
import traceback
import logging

flags.DEFINE_string('event_file_path', None, 'Path to event file to insert into database')
FLAGS = flags.FLAGS

def read_event_file(pp, db, base_query, file_name=None):
    if file_name is None:
        tf.logging.info("file_name was none, doing nothing")
    else:
        try:
            db.open_connection()
            for ev in tf.train.summary_iterator(file_name):

                #could use step and wall_time for something
                out = {}
                out['step'] = ev.step
                out['wall_time'] = ev.wall_time
                tag_val = {}
                #

                for v in ev.summary.value:
                    try:
                        tag_val[v.tag] = v.simple_value
                    except AttributeError:
                        tf.logging.error("could not get %s from: %s" % ("simple_value", v.tag))
                
                lr = u'learning_rate'
                try:                    
                    if tag_val[lr] is None:
                        continue
                except KeyError as ke:
                    tf.logging.info('could not find %s, will not insert for this file' % (lr))
                else:                    
                    db.execute(base_query, (1, 1, tag_val[lr]))
                    tf.logging.info('successfully inserted: ' + str(tag_val[lr]))
        except:
            traceback.print_exc()
        finally:
            db.close_connection()

def main(unused_argv):
    database = db_lib.Database()
    pp = pprint.PrettyPrinter(indent=4)
    read_event_file(pp, database, db_lib.INSERT_QUERY, FLAGS.event_file_path)

if __name__ == '__main__':
    #make logs show up on stdout
    logging.getLogger("tensorflow").setLevel(logging.INFO)

    tf.app.run()


