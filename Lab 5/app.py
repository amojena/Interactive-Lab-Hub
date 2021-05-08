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

def getMean(l):
    m= float(sum(l)) / float(len(l))
    return "{:.2f}".format(m)

def formatPeaks(p):
    return "({:.2f}, {:.2f})".format(p[0], p[1])


if __name__ == "__main__":
    os.system("clear")

    xPeak, yPeak, zPeak = [0,0], [0,0], [0,0]
    backlines = "\033[F"*2

    threshold = int(input("Threshold value: "))
    nBlocks = int(input("Blocks for running average: "))

    x = [0] * nBlocks
    y = [0] * nBlocks
    z = [0] * nBlocks

    while True:
        tempAcc = mpu.acceleration

        # update running average list
        x = x[1:] + [tempAcc[0]]
        y = y[1:] + [tempAcc[1]]
        z = z[1:] + [tempAcc[2]]

        # peak identification
        xPeak = updatePeak(xPeak, tempAcc[0])
        yPeak = updatePeak(yPeak, tempAcc[1])
        zPeak = updatePeak(zPeak, tempAcc[2])


        print(f"Threshold exceeded - X: {tempAcc[0] > threshold}, Y: {tempAcc[1] > threshold}, Z: {tempAcc[2] > threshold}")
        print(f"Average of last {nBlocks}s: ({getMean(x)},{getMean(y)},{getMean(z)})")
        print(f"Peaks X: {formatPeaks(xPeak)}, Y: {formatPeaks(yPeak)}, Z: {formatPeaks(zPeak)}{backlines}\r",end="", flush=True)

        time.sleep(1)