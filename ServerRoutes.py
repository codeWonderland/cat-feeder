import time

from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse

from StorageProtocol import StorageProtocol
from FoodManager import dispenceFood, getLastFeedingData, getNextFeedingTime


class RoutingProtocol:
    def __init__(self, server):

        # === HTML Routes ===

        @server.route("/")
        def base(request: HTTPRequest):
            with HTTPResponse(
                    request,
                    content_type=MIMEType.TYPE_HTML
            ) as response:
                response.send_file("index.html")

        @server.route("/update")
        def update(request: HTTPRequest):
            with HTTPResponse(
                    request,
                    content_type=MIMEType.TYPE_HTML
            ) as response:
                response.send_file("update.html")

        # === API ROUTES ===

        @server.route("/server-time")
        def server_time(request: HTTPRequest):
            with HTTPResponse(request) as response:
                localtime = time.localtime()
                localminutes = str(localtime[4])

                if len(localminutes) == 1:
                    localminutes = '0' + localminutes

                data = "{}:{}".format(localtime[3], localminutes)
                response.send(data, content_type="text/plain")

        @server.route("/feeding-time")
        def feeding_time(request: HTTPRequest):
            with HTTPResponse(request) as response:
                last_feeding_data = getLastFeedingData()
                next_feeding_time = getNextFeedingTime(last_feeding_data[1])
                response.send(next_feeding_time, content_type="text/plain")

        @server.route("/feed", HTTPMethod.POST)
        def feed(request: HTTPRequest):
            dispenceFood()

            with HTTPResponse(request) as response:
                response.send("ok", content_type="text/plain")

        @server.route("/set-feeding-time", HTTPMethod.POST)
        def set_feeding_time(request: HTTPRequest):
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

            with HTTPResponse(request) as response:
                response.send("ok", content_type="text/plain")

        @server.route("/get-feeding-date")
        def get_feeding_date(request: HTTPRequest):
            with HTTPResponse(request) as response:
                last_feeding_data = getLastFeedingData()
                response.send(last_feeding_data[0], content_type="text/plain")
