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


def formatTime(tim):
    secs = tim % 60
    mins = tim//60
    hours = mins//60

    return "{:0>2d}h {:0>2d}m {:0>2d}s".format(int(hours), int(mins), int(secs))

def stopwatch():

    print("stopwatch")
    time.sleep(1)
    done = False
    started = False
    paused = False

    hour = 0
    mins = 0
    secs = 0

    lastPaused = 0.0
    pauseOffset = 0.0
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        if started is False:
            stopwatchText = "00h 00m 00s"

        elif not paused:
            stopwatchText = formatTime(time.time()-start_time - pauseOffset)
            print(stopwatchText, end="", flush=True)
            print("\r", flush=True, end="")

        elif paused:
            pauseOffset += time.time()-lastPaused


        draw.text((0,30), stopwatchText, font=font, filler="#FFFFFF")


        if buttonB.value and not buttonA.value:
            if started is False:
                started = True
                start_time = time.time()
                done, paused = False, False
                hour = 0
                mins = 0
                secs = 0
                lastPaused = 0.0
                pauseOffset = 0.0

            elif not paused:
                lastPaused = time.time()
                paused = True

            elif paused:
                paused = False



        if buttonA.value and not buttonB.value:
            print("derp")
            if not started:
                done = True
            elif paused:
                started = False
            elif not paused:
                paused = True

        if done:
            break

        disp.image(image, rotation)
        time.sleep(1)

def main():

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

        dispTime = f"{hour}:{mins}"


        draw.text((x, -5), dispTime, font=bigFont, fill=white)

        timeZonePos = (x + 65, bigFont.getsize(dispTime)[1] + 12)
        draw.text(timeZonePos, timeZone, font=font, fill="#FFFF00")

        date_abr = f"{month} {dayNum}"
        datePos = list(timeZonePos)
        datePos[0] = timeZonePos[0] + font.getsize(timeZone)[0] + 10
        datePos = tuple(datePos)
        draw.text(datePos, date_abr, font=font, fill="#00FFFF")



        y_pie =bigFont.getsize(dispTime)[1]
        x0, y0 = 5, y_pie
        x1 = 60
        y1 = y0 + x1-x0
        pie_bound = [(x0, y0), (x1, y1)]
        draw.pieslice(pie_bound, 0, int(sec) * 6, white)
        sx = (x1+x0)/2
        sy = (y1+y0)/2
        draw.text((sx-17, sy-15), sec, font=font, fill="#FF0000")


        if buttonB.value and not buttonA.value:
            timeIndex = (timeIndex + 1) % 4

        if buttonA.value and not buttonB.value:
            stopwatch()

        # Display image.
        disp.image(image, rotation)
        time.sleep(1)

main()
