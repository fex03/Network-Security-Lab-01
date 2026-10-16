# HTTP: mini API
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

PORT = 8080

# Subclass of BaseHTTPRequestHandler
class MyReqHandler(BaseHTTPRequestHandler):
    
    # Modify do_GET method to have desired behaviour
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers() # Must be called to send the empty line that terminates the header section
        else:
            self.send_response(404)
            self.end_headers()
    
# Instantiate server and run it
server = HTTPServer(('', PORT), MyReqHandler)
print("Server is listening on port 8080...")

# Blocking function: listening http requests from clients
server.serve_forever()
