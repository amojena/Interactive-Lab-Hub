import time
import board
import busio
import adafruit_mpu6050
import sys
import os


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

    xTotal, yTotal, zTotal = 0, 0, 0
    xPeak, yPeak, zPeak = [0,0], [0,0], [0,0]

    round = 1
    threshold = 5 # arbitrary
    backlines = "\033[F"*2

    threshold = int(input("Threshold value: "))
    nBlocks = int(input("Blocks for running average: "))

    while True:
        tempAcc = mpu.acceleration
        xTotal += tempAcc[0]
        yTotal += tempAcc[1]
        zTotal += tempAcc[2]

        print(f"Threshold exceeded - X: {tempAcc[0] > threshold}, Y: {tempAcc[1] > threshold}, Z: {tempAcc[2] > threshold}")

        print(f"Average after {round}s: ({xTotal/round},{yTotal/round},{zTotal/round})")
        round += 1

        xPeak = updatePeak(xPeak, tempAcc[0])
        yPeak = updatePeak(yPeak, tempAcc[1])
        zPeak = updatePeak(zPeak, tempAcc[2])

        print(f"Peaks X: {xPeak}, Y: {yPeak}, Z: {zPeak}{backlines}\r",end="", flush=True)

        time.sleep(1)
