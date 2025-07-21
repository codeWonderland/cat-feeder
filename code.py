import os
import socketpool
import wifi
import adafruit_ntp
import rtc
import time

from adafruit_httpserver.server import HTTPServer
from ServerRoutes import RoutingProtocol
from StorageProtocol import StorageProtocol
from FoodManager import checkFeedTime


# Connect to wifi
ssid = os.getenv('WIFI_SSID')
print("Connecting to", ssid)
wifi.radio.connect(ssid, os.getenv('WIFI_PASSWORD'))
print("Connected to", ssid)

# set up socketpool and server
pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

# sync system time with EDT
my_tz_offset = -4  # EDT
ntp = adafruit_ntp.NTP(pool, tz_offset=my_tz_offset)
rtc.RTC().datetime = ntp.datetime

# establish server routes for updates
routing = RoutingProtocol(server)

# Start the server.
print(f"Listening on http://{wifi.radio.ipv4_address}:80")
server.start(str(wifi.radio.ipv4_address))

# create variable to slow to down feedtime checks
next_feedtime_check = time.time()


while True:
    try:
        # determine if we need to feed Milk
        current_time = time.time()

        if current_time >= next_feedtime_check:
            next_feedtime_check = current_time + 60

            checkFeedTime()


        # Process any waiting web requests
        server.poll()

    except OSError as error:
        print(error)
        continue
