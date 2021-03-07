import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from image_fn import main


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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 85)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# main("galxy.jpg")

fills = ["#FFFFFF", "#000000"]
white = "#FFFFFF"
filler = 0

timeIndex = 0

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py
    y = 5
    # cmd = "date"
    # TIME = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # draw.text((x, y), TIME, font=font, fill=fills[filler%2])
    # y += font.getsize(TIME)[1]
    # draw.text((x, y), TIME, font=font, fill=fills[(filler+1)%2])


    cmd = "TZ=\":US/Eastern\" date"
    EST_TIME = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "TZ=\":US/Pacific\" date"
    PST_TIME = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "TZ=\":US/Mountain\" date"
    MST_TIME = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "TZ=\":US/Central\" date"
    CET_TIME = subprocess.check_output(cmd, shell=True).decode("utf-8")

    times = [EST_TIME, PST_TIME, MST_TIME, CET_TIME]

    _, dayNum, month, year,  tim, _, timeZone = times[timeIndex].split()
    hour, mins, sec = tim.split(":")
    hour = str((int(hour) + 12) % 24)
    # print(times[timeIndex].split())


    draw.text((x, 2), hour, font=bigFont, fill=white)
    draw.text((x, 20), timeZone, font=font, fill=white)


    if buttonA.value:
        timeIndex = (timeIndex + 1) % 4
        print("A")

    if buttonB.value:
        timeIndex = (timeIndex - 1) % 4
        print("B")


    filler += 1 % 2

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
