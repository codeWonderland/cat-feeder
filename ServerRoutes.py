import time

from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse

from StorageProtocol import StorageProtocol
from FoodManager import dispenceFood


class RoutingProtocol:
    def __init__(self, server):
        @server.route("/")
        def base(request: HTTPRequest):
            """
            Serve the default index.html file.
            """
            with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
                response.send_file("index.html")


        @server.route("/server-time")
        def base(request: HTTPRequest):
            with HTTPResponse(request) as response:
                localtime = time.localtime()
                localminutes = str(localtime[4])
                if len(localminutes) == 1: localminutes = '0' + localminutes
                data = "{}:{}".format(localtime[3], localminutes)
                print("Server time request:")
                print(data)
                response.send(data, content_type="text/plain")


        @server.route("/feeding-time")
        def base(request: HTTPRequest):
            with HTTPResponse(request) as response:
                sp = StorageProtocol()
                feeding_time_array = sp.read("feeding_time.txt")
                response.send(feeding_time_array[0], content_type="text/plain")


        @server.route("/feed", HTTPMethod.POST)
        def feed_fn(request: HTTPRequest):
            print('/feed was pinged!')
            print('response: 200 OK')

            dispenceFood()
            
            with HTTPResponse(request) as response:
                response.send("ok", content_type="text/plain")


        @server.route("/update")
        def base(request: HTTPRequest):
            """
            Serve the default index.html file.
            """
            with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
                response.send_file("update.html")


        @server.route("/set-feeding-time", HTTPMethod.POST)
        def base(request: HTTPRequest):
            print("/set-feeding-time was pinged!")
            new_feeding_time = request.body
            print("New Time:")
            print(request.body)
            sp = StorageProtocol()
            sp.write("feeding_time.txt", new_feeding_time)

            with HTTPResponse(request) as response:
                response.send("ok", content_type="text/plain")


        @server.route("/get-feeding-date")
        def base(request: HTTPRequest):
            with HTTPResponse(request) as response:
                sp = StorageProtocol()
                feeding_date_array = sp.read("last_feed_date.txt")
                response.send(feeding_date_array[0], content_type="text/plain")


        @server.route("/set-feeding-date", HTTPMethod.POST)
        def base(request: HTTPRequest):
            print("/set-feeding-date was pinged!")
            new_feeding_date = request.body
            print("New date:")
            print(request.body)
            sp = StorageProtocol()
            sp.write("last_feed_date.txt", new_feeding_date)

            with HTTPResponse(request) as response:
                response.send("ok", content_type="text/plain")