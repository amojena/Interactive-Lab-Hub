import Time
import os
import system
import numpy as np
import subprocess

CONFIDENCE_THRESHOLD = 0.5
PERSISTANCE_THRESHOLD = 0.5


from rpi_vision.agent.capture import PiCameraStream
from rpi_vision.models.teachablemachine import TeachableMachine

capture_manager = PiCameraStream(resolution=(screen.get_width(), screen.get_height()), rotation=180, preview=False)

if __name__ == '__main__':
    model = TeachableMachine('transfer/converted_savedmodel.zip')
    capture_manager.start()

    while not capture.manager_stopped:
        print("Cam working")
