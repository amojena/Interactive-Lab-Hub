import time
import os
import system
import numpy as np
import subprocess
import tensorflow.keras as tf

if __name__ == '__main__':
    savedModelPath = "/transfer/converted_savedmodel/model.savemodel/saved_model.pb"
    tf.models.load_model(savedModelPath)
