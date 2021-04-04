import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from random import randint


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
rotation = 90

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
    def __init__(self, pos, color):
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = pos[2]
        self.y2 = pos[3]
        self.speed = 15
        self.color = color
        print("Circle is color: {}".format(self.color))


    def moveDown(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

    def getPos(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def getColor(self):
        return self.color

def drawOriginCircles():
    y2 = [y + offset* i for i in range(4)]
    for i in range(4):
        draw.ellipse([(x, y2), (x+radius, y2 + radius)], fill=fill_colors[i], outline="#FFFFFF")




def main():
    x, y = 215, 5
    radius = 20
    offset = 34
    fill_colors = ["#67ee8a", "#aeb1f9", "#f6acbb", "#eb9f2a"]
    circle_start_pos = [(x, y + offset * i, x + radius, (y + offset * i)+radius) for i in range(4)]

    topCircles = [Circle(circle_start_pos[i], fill_colors[i]) for i in range(4)]
    activeCircles = []


    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)


        for circle in topCircles:
            draw.ellipse(circle.getPos, fill=circle.getColor, outline="#FFFFFF")

        for circle in activeCircles:
            draw.ellipse(circle.getPos, fill=circle.getColor, outline="#FFFFFF")
            circle.moveDown()

        if randint(1,10) <= 3:
            ind = randint(0,3)
            activeCircles.append(Circle(circle_start_pos[ind], fill_colors[ind]))


        # Display image.
        disp.image(image, rotation)
        time.sleep(1)

main()
