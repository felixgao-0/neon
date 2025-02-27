import time
import math
import datetime

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import board
import displayio
import vectorio
import framebufferio
import rgbmatrix
import terminalio

import requests

# Setup start
# Leave as 1 unless scrolling felix, bigger = faster scrolling in the loop
TIMER_MULTIPLE = 1
TTC_ROUTE_URL = "[change this! I redacted this for privacy reasons]"
font = bitmap_font.load_font("tom-thumb.bdf")

def scroll(line, overlap=10):
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width# - 10

def get_eastern_time():
    # Edited from code off chatgpt bc i hate timezones and have no clue how on earth to make that stuff work :(
    now = datetime.datetime.now()

    dst_start = datetime.datetime(now.year, 3, 8)
    dst_start += datetime.timedelta(days=(6 - dst_start.weekday()))

    dst_end = datetime.datetime(now.year, 11, 1)
    dst_end += datetime.timedelta(days=(6 - dst_end.weekday()))

    if dst_start <= now < dst_end:
        offset = datetime.timedelta(hours=-4)
    else:
        offset = datetime.timedelta(hours=-5)

    return now + offset


displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.IO1, board.IO2, board.IO3, board.IO5, board.IO4, board.IO6],
    addr_pins=[board.IO8, board.IO7, board.IO10, board.IO9],
    clock_pin=board.IO12, latch_pin=board.IO11, output_enable_pin=board.IO13)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

# Setup end
def scroll(line):
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width - 5
        

header = label.Label(
    terminalio.FONT,
    text="Schedule:",
    color=0xDB2018
)
header.x = 2
header.y = 5

update_timer = label.Label(
    font,
    text="__",
    color=0xFCFF1E
)
update_timer.x = 57
update_timer.y = 30

date = label.Label(
    font,
    text="[__]",
    color=0xFCFF1E
)
date.x = 2
date.y = 30

arrival_times = label.Label(
    font,
    text="[__Loading__]",
    color=0xFFFFFF
)
arrival_times.x = 2
arrival_times.y = 15

main_group = displayio.Group()
display.root_group = main_group
main_group.append(header)
main_group.append(update_timer)
main_group.append(date)
main_group.append(arrival_times)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
#    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'www.ttc.ca',
}


display_timing = True # alternate between fullness scale and time until arrival
#time_adjust = abs(int(get_eastern_time().strftime('%S')) - 30) # Adjust to sync to 30 second irl intervals
while True:
    try:
        print("Fetching Update")
        r = requests.get(TTC_ROUTE_URL, headers=headers)
        r.raise_for_status()
        result = r.json()
        print(result)

        scroll(date)

        # - int(get_eastern_time().strftime('%S')))*TIMER_MULTIPLE
        for time_remaining in range(30*TIMER_MULTIPLE, 0, -1):
            update_timer.text = str(math.ceil(time_remaining/TIMER_MULTIPLE))
            date.text = get_eastern_time().strftime("%I:%M:%S") # %b %-d

            if time_remaining % (5*TIMER_MULTIPLE) == 0:
                arrival_times.text = ""
                if display_timing == True:
                    for timing in result:
                        arrival_times.text += timing["nextBusMinutes"] + " minutes\n" if timing["nextBusMinutes"] != "D" else "delayed"
                else:
                    for timing in result:
                        arrival_times.text += timing["crowdingIndex"] + "/3 full\n"
                display_timing = not display_timing # flip around for next time
                                           
            time.sleep(1/TIMER_MULTIPLE)
            
    except Exception as error:
        print(error)
        error_text = label.Label(
            terminalio.FONT,
            text="[Error]\n" + error,
            color=0xDB2018
        )
        error_text.x = 3
        error_text.y = 7

        error_group = displayio.Group()
        error_group.append(error_text)
        display.root_group = error_group

        raise error # stop the code in its tracks :(
