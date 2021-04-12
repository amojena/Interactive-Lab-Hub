import time
import board
import busio
import adafruit_mpu6050
import sys
import os
import numpy as np


i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

def updatePeak(peak, acc):
    if peak[1] > acc:
        return (peak[0], acc)
    elif peak[0] < acc:
        return (acc, peak[1])
    return peak



if __name__ == "__main__":
    os.system("clear")

    xPeak, yPeak, zPeak = [0,0], [0,0], [0,0]

    round = 1
    threshold = 5 # arbitrary
    backlines = "\033[F"*2

    threshold = int(input("Threshold value: "))
    nBlocks = int(input("Blocks for running average: "))

    x = [0] * nBlocks
    y = [0] * nBlocks
    z = [0] * nBlocks

    mean = lambda x: round(float(sum(x)) / float(len(x)), 2)

    while True:
        tempAcc = mpu.acceleration

        x = x[1:] + [tempAcc[0]]
        y = y[1:] + [tempAcc[1]]
        z = z[1:] + [tempAcc[2]]

        print(f"Threshold exceeded - X: {tempAcc[0] > threshold}, Y: {tempAcc[1] > threshold}, Z: {tempAcc[2] > threshold}")

        print(f"Average of last {nBlocks}s: ({mean(x)},{mean(y)},{mean(z)})")
        round += 1

        xPeak = updatePeak(xPeak, tempAcc[0])
        yPeak = updatePeak(yPeak, tempAcc[1])
        zPeak = updatePeak(zPeak, tempAcc[2])

        print(f"Peaks X: {round(xPeak, 2)}, Y: {round(yPeak, 2)}, Z: {round(zPeak, 2)}{backlines}\r",end="", flush=True)

        time.sleep(1)
