from time import sleep
import os
import sys
import numpy as np
import tensorflow.keras as tf
from PIL import Image, ImageOps

labels = {0: "Previous", 1: "Next", 2: "Pause/Play", 3: "Neutral"}

savedModelPath = "transfer/converted_keras/keras_model.h5"
model = tf.models.load_model(savedModelPath)

# what is the prediction and is the model confidece higher than the threshold
def interpret(prediction, threshold):
    p = -1
    pi = -1
    for i, val in enumerate(prediction[0]):
        if val > p:
            p = val
            pi = i
    
    return (labels[pi], (p*100) > threshold)

# take picture, analyze, and return prediction w confidence value
def get_action(threshold):
    img_file = "temp.jpg"
    cmd = "fswebcam " + img_file
    
    sleep(2)
    # take picture
    os.system(cmd)
    
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(img_file)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return interpret(prediction, threshold)
    
