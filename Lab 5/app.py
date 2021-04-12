import eventlet
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

    x_total, y_total, z_total = 0, 0, 0
    xPeak, yPeak, zPeak = [0,0], [0,0], [0,0]

    round = 1
    threshold = 5 # arbitrary
    while True:
        x_total, y_total, z_total += mpu.acceleration
        print(f"Average after {round}s: ({x_total/round},{y_total/round},{z_total/round})")
        round += 1

        xPeak = updatePeak(xPeak, mpu.acceleration[0])
        xPeak = updatePeak(yPeak, mpu.acceleration[1])
        xPeak = updatePeak(zPeak, mpu.acceleration[2])

        print(f"Peaks X: {xPeak}, Y: {yPeak}, Z: {zPeak}\r", end="")
