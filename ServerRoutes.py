import time

from adafruit_httpserver import (
    methods,
    Request,
    Response
)

from StorageProtocol import StorageProtocol
from FoodManager import dispenceFood, getLastFeedingData, getNextFeedingTime


class RoutingProtocol:
    def __init__(self, server):

        # === HTML Routes ===

        @server.route("/")
        def base(request: Request):
            with Response(
                    request,
                    content_type="text/html"
            ) as response:
                response.send_file("index.html")

        @server.route("/update")
        def update(request: Request):
            with Response(
                    request,
                    content_type="text/html"
            ) as response:
                response.send_file("update.html")

        # === API ROUTES ===

        @server.route("/server-time")
        def server_time(request: Request):
            with Response(request) as response:
                localtime = time.localtime()
                localminutes = str(localtime[4])

                if len(localminutes) == 1:
                    localminutes = '0' + localminutes

                data = "{}:{}".format(localtime[3], localminutes)
                response.send(data, content_type="text/plain")

        @server.route("/feeding-time")
        def feeding_time(request: Request):
            with Response(request) as response:
                last_feeding_data = getLastFeedingData()
                next_feeding_time = getNextFeedingTime(last_feeding_data[1])
                response.send(next_feeding_time, content_type="text/plain")

        @server.route("/feed", methods.POST)
        def feed(request: Request):
            dispenceFood()

            with Response(request) as response:
                response.send("ok", content_type="text/plain")

        @server.route("/set-feeding-time", methods.POST)
        def set_feeding_time(request: Request):
            new_feeding_times = request.body
            new_feeding_times = new_feeding_times.split(',')
            sp = StorageProtocol()

            first_entry = True
            for feeding_time in new_feeding_times:
                if first_entry:
                    sp.write("feeding_time.txt", feeding_time)
                    first_entry = False
                else:
                    sp.write("feeding_time.txt", feeding_time, "a")

            with Response(request) as response:
                response.send("ok", content_type="text/plain")

        @server.route("/get-feeding-date")
        def get_feeding_date(request: Request):
            with Response(request) as response:
                last_feeding_data = getLastFeedingData()
                response.send(last_feeding_data[0], content_type="text/plain")
