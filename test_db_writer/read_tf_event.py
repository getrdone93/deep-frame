import tensorflow as tf

def read_event_file(file_name=None, types=(float, bytes)):
    if file_name is None:
        print("file_name was none, doing nothing")
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
                    print("ERROR: could not get %s from: %s" % ("simple_value", v.tag))

            out['tag_val'] = tag_val

            print(out)
            print

if __name__ == '__main__':
    read_event_file("/home/tanderson/graduateWork/project/framework/data/model_cp/ssd_mobilenet_v1_coco/model/eval_0/events.out.tfevents.1558898299.6acf4ea16b37")
