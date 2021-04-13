import time
import os
import sys
import numpy as np
import subprocess
import tensorflow.keras as tf
from picamera import PiCamera
from PIL import Image, ImageOps

labels = {0: "Previous", 1: "Next", 2: "Stop", 3: "Play", 4: "Neutral"}

def interpret(prediction):
    p = -1
    pi = -1
    for i, val in enumerate(prediction[0]):
        if val > p:
            p = val
            pi = i
    
    print(f"{labels[pi]}: {p*100}%")

if __name__ == '__main__':
    print("Loading...")
    
    savedModelPath = "transfer/converted_keras/keras_model.h5"
    model = tf.models.load_model(savedModelPath)

    
    img_file = "test2.jpg"
    cmd = "fswebcam " + img_file
    for i in range(5):
        time.sleep(3)
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

        # display the resized image
        #image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        print(prediction)
        interpret(prediction)
        print()
        print()
    
