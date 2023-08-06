"""tbev.

Usage:
    tbev demo 
    tbev <pickle_file> [--logdir=<path>]

Options:
    -h --h    Show help screen
    --logdir=<path>  Location to store log files [default: ./logs/]

"""

from docopt import docopt
args = docopt(__doc__)


import sys
from colorama import init, deinit, Fore, Back, Style
init()


def print_info(s):
    print(Fore.GREEN+"[INFO] "+Style.RESET_ALL+s)

def print_warning(s):
    print(Fore.YELLOW+"[WARNING] "+Style.RESET_ALL+s)

def print_error(s, terminate=False):
    print(Fore.RED+"[ERROR] "+Style.RESET_ALL+s)
    if terminate:
        sys.exit()

import pickle
print_info("Loading tensorflow")
try:
    import tensorflow as tf
except ImportError:
    print_error("Could not import tensorflow. Make sure it is installed", True)

try:
    import cv2
except ImportError:
    print_error("Could not import Opencv (cv2). Make sure it is installed", True)

try:
    import numpy as np
except ImportError:
    print_error("Could not import Numpy. Make sure it is installed", True)

from tensorboard import main as tb
from tensorflow.contrib.tensorboard.plugins import projector
import os
import math
import urllib.request
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def get_static_file_path(filename):
    return os.path.join(os.path.dirname(__file__),filename)


def create_sprites(image_paths,sprite_path,sprite_size):
    num_images = len(image_paths)
    # print(num_images)
    sprite_num_rows = math.ceil(math.sqrt(num_images))
    sprite_height, sprite_width = sprite_size
    sprite_image_obj = np.ones(shape=((sprite_num_rows)*sprite_height,(sprite_num_rows)*sprite_width,3),dtype=np.uint8)*255
    for i,image_path in enumerate(image_paths):
        if not os.path.exists(image_path):
            image_path = get_static_file_path("not_found.png")
        try:
            image_obj = cv2.imread(image_path)
            image_obj = cv2.resize(image_obj, (sprite_height,sprite_width))
        except:
            image_obj = cv2.imread(get_static_file_path("invalid.png"))
            image_obj = cv2.resize(image_obj, (sprite_height,sprite_width))
        x = (i%sprite_num_rows)*sprite_width
        y = (i//sprite_num_rows)*sprite_height
        sprite_image_obj[y:y+sprite_height,x:x+sprite_width] = image_obj
        
    cv2.imwrite(sprite_path,sprite_image_obj)


def verify_embeddings_dict(embeddings_dict):
    try:
        embddings = embeddings_dict["embedding"]
    except KeyError:
        print_error("Embeddings not found in pickle file", True)
    
    try:
        labels = embeddings_dict["labels"]
    except KeyError:
        print_error("Labels not found in pickle file", True)
    
    num_samples = len(embddings)

    if "sprite_paths" in embeddings_dict:
        sprite_paths_len = len(embeddings_dict["sprite_paths"])
        if sprite_paths_len != num_samples:
            print_error("Number of sprite paths is not equal to number of embeddings: {} != {}".format(sprite_paths_len,
                                                                                                       num_samples))
        for sprite_path in embeddings_dict["sprite_paths"]:
            if not os.path.exists(sprite_path):
                print_warning("Sprite image path {} not found".format(sprite_path))

    for label in labels:
        if len(labels[label]) != num_samples:
            print_error("Number of labels: {} is not equal to number of embeddings: {} != {}".format(label,
                                                                                                     len(labels[label]),
                                                                                                     num_samples), True)
    



def generate_embeddings_from_pickle(pickle_path, logdir):
    print_info("Loading embeddings pickle")
    embeddings_dict = pickle.load(open(pickle_path,"rb"))
    print_info("Verifying embeddings")
    verify_embeddings_dict(embeddings_dict)
    print_info("Embeddings verified successfully")
    embedding_variable = tf.Variable(embeddings_dict['embedding'], name="embeddings")

    summary_writer = tf.summary.FileWriter(logdir)
    config = projector.ProjectorConfig()
    embedding = config.embeddings.add()
    embedding.tensor_name = embedding_variable.name
    embedding.metadata_path = 'metadata.tsv'
    if "sprite_paths" in embeddings_dict:
        sprite_path = os.path.join(logdir,"sprites.png")
        sprite_size = [100,100]
        create_sprites(embeddings_dict["sprite_paths"],sprite_path,sprite_size)
        embedding.sprite.image_path = "sprites.png"
        embedding.sprite.single_image_dim.extend(sprite_size)
    projector.visualize_embeddings(summary_writer, config)

    print_info("Creating embeddings checkpoint")

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.save(sess, os.path.join(logdir,'model.ckpt'), 0)

        labels = embeddings_dict["labels"]

        labels_types = list(labels.keys())
        labels_values = []
        for i in range(len(labels[labels_types[0]])):
            labels_values_list = []
            for label_type in labels:
                labels_values_list.append(str(labels[label_type][i]))
            labels_values.append(labels_values_list)
        
        # print(labels_values)
        print_info("Creating labels metadata")
        with open(os.path.join(logdir,embedding.metadata_path), 'w') as handle:
            if len(labels_types) > 1:
                handle.write("{}\n".format("\t".join(labels_types)))
            for label_value in labels_values:
                handle.write('{}\n'.format("\t".join(label_value)))
    
    print_info("Logs created at {}".format(os.path.abspath(logdir)))


def main():
    if args["demo"]:
        generate_embeddings_from_pickle(get_static_file_path("./demo_word2vec_embeddings_zen.pkl"),"./logs/")
    else:
        generate_embeddings_from_pickle(args["<pickle_file>"],args["--logdir"])

        

if __name__ == '__main__':
    # print(args)
    main()