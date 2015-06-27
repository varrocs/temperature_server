from tornado import tcpserver
from tornado.ioloop import IOLoop
import tornado
import tornado.template
import tornado.web
import re
import datastore

class StreamHandler():
    def __init__(self, owner, stream, callback):
        self.owner = owner
        self.stream = stream
        self.regexp=re.compile("Temp: ([0-9.]*); Hum: ([0-9.]*)")
        self.callback=callback

    def _parse_data(self, data):
        m = self.regexp.search(str(data))
        return m.group(1, 2) if m else None

    def _data_ready(self, data):
        result = self._parse_data(data)
        print("Read data {}, parsed data: {}".format(data, str(result)))
        if result:
            self.callback(result)
        self.stream.close()
        self.owner.stream_finished(self)

    def handle(self):
        self.stream.read_until(b'\n', self._data_ready)

class TemperatureServer(tcpserver.TCPServer):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.streams=[]

    def handle_stream(self, stream, address):
        s = StreamHandler(self, stream, self.callback)
        self.streams.append(s)
        s.handle()

    def stream_finished(self, stream):
        self.streams.remove(stream)

#####################################################################

PATH_INDEX="static/index.html"
PATH_GRAPH="graph.svg"

class CurrentHandler(tornado.web.RequestHandler):
    def get(self):
        result= datastore.last_n(1)[0]
        self.write( {'temperature': result['temperature'], 'humidity': result['humidity'] })

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        result= datastore.last_n(1)[0]
        loader = tornado.template.Loader('static')
        result = loader.load('index.html').generate(temperature=result['temperature'], humidity=result['humidity'])
        self.write(result)

def start_server(web_port, tcp_port, callback):
    server = TemperatureServer(callback)
    print("TCP Listening on port {}".format(tcp_port))
    server.listen(tcp_port)
    server.start()

    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/current", CurrentHandler),
        (r"/graph/(.*)", tornado.web.StaticFileHandler, {'path': "graph"}),
    ])
    print("WEB Listening on port {}".format(web_port))
    application.listen(web_port)

    IOLoop.current().start()