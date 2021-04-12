import time
import os
import sys
import numpy as np
import subprocess
import tensorflow.keras as tf

if __name__ == '__main__':
    print("Loading...")
    savedModelPath = "transfer/converted_savedmodel/model.savedmodel/"
    tf.models.load_model(savedModelPath)
    print("Yay")
