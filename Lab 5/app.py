import time
import board
import busio
import adafruit_mpu6050
import sys


i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

def updatePeak(peak, acc):
    if peak[1] > acc:
        return (peak[0], acc)
    elif peak[0] < acc:
        return (acc, peak[1])
    return peak



if __name__ == "__main__":

    xTotal, yTotal, zTotal = 0, 0, 0
    xPeak, yPeak, zPeak = [0,0], [0,0], [0,0]

    round = 1
    threshold = 5 # arbitrary
    while True:
        xTotal += mpu.acceleration[0]
        yTotal += mpu.acceleration[1]
        zTotal += mpu.acceleration[2]

        xPeak = updatePeak(xPeak, mpu.acceleration[0])
        yPeak = updatePeak(yPeak, mpu.acceleration[1])
        zPeak = updatePeak(zPeak, mpu.acceleration[2])

        print(f"Average after {round}s: ({xTotal/round},{yTotal/round},{zTotal/round})\nPeaks X: {xPeak}, Y: {yPeak}, Z: {zPeak}\r", end ="")
        round += 1
        time.sleep(1)
