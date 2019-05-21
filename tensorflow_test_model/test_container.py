import tensorflow as tf
from absl import flags

flags.DEFINE_string(
    'model_dir', None, 'Path to output model directory '
    'where event and checkpoint files will be written.')
flags.DEFINE_string('pipeline_config_path', None, 'Path to pipeline config '
                    'file.')
FLAGS = flags.FLAGS

def main(unused_argv):
    flags.mark_flag_as_required('model_dir')
    flags.mark_flag_as_required('pipeline_config_path')

    print("I made it here, flags ", FLAGS.model_dir, FLAGS.pipeline_config_path)

    f = open("/data/test_file.txt", "a")
    f.write("This is some dater")
    f.close()

if __name__ == '__main__':
    tf.app.run()
