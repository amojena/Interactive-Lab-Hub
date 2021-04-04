import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from random import randint
import busio

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 270

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 85)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

class Circle:
    def __init__(self, pos, color, id):
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = pos[2]
        self.y2 = pos[3]
        self.speed = 18 # rate at which circle will move down the screen
        self.color = color
        self.id = id # column # used to compare with button pressed

    def moveDown(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

    def getPos(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def getCenterX(self):
        return (self.x2 + self.x1)/2

    def getColor(self):
        return self.color

    def draw(self):
        draw.ellipse(self.getPos(), fill=self.color, outline="#FFFFFF")

    def getID(self):
        return self.id


def main():
    x, y = 215, 5
    radius = 20
    offset = 34
    fill_colors = ["#67ee8a", "#aeb1f9", "#f6acbb", "#eb9f2a"]
    circle_start_pos = [(x, y + offset * i, x + radius, (y + offset * i)+radius) for i in range(4)]
    action_w, action_h = 26, 134

    topCircles = [Circle(circle_start_pos[i], fill_colors[i], i) for i in range(4)]
    activeCircles = []


    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill="#DFE3EC")
        draw.rectangle((0, 0, action_w, action_h), outline="#A70000")

        for circle in topCircles:
            circle.draw()

        for circle in activeCircles:
            circle.draw()
            circle.moveDown()

        # 50% chance of a new circle spawning
        if randint(1,10) <= 6:
            ind = randint(0,3)
            activeCircles.append(Circle(circle_start_pos[ind], fill_colors[ind], ind))

        ## TODO: if circle has reached end of screen, remove from list to stop render
        if len(activeCircles) >= 1 and activeCircles[0].getCenterX() <= action_w/2:

            for i in range(12):
                if mpr121[i].value:
                    print(f"Banana {i} touched!")
            # check if the appropriate button is pressed by now
                # green led and score += 1 if yes
                # red led if no
            activeCircles.pop(0)


        # Display image.
        disp.image(image, rotation)
        time.sleep(0.7)

main()
