from gevent.pywsgi import WSGIServer
import app

server = WSGIServer(('', 80), app)
server.serve_forever()