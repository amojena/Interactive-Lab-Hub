import time
import os
import sys
import numpy as np
import subprocess
import tensorflow.keras as tf
from picamera import picCamera

if __name__ == '__main__':
    print("Loading...")
    savedModelPath = "transfer/converted_keras/keras_model.h5"
    model = tf.models.load_model(savedModelPath)

    cam = PiCamera()

    cam.capture('test.jpg')
    print("Yay")
