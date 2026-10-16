# HTTP: mini API
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

PORT = 8080

# Subclass of BaseHTTPRequestHandler
class MyReqHandler(BaseHTTPRequestHandler):
    
    # Modify do_GET method to have desired behaviour
    def do_GET(self):
        
        # I divide self.path raw string in the path and the query so I can check correctly the input command
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        
        if path == '/':
            self.send_response(200)
            self.end_headers() # Must be called to send the empty line that terminates the header section
        
        elif path == '/echo':
            params = urllib.parse.parse_qs(query) # Returns values inside a list: e.g. params becomes {'msg': ['hello world']}
            
            text = ""
            
            if 'msg' in params:
                text = params['msg'][0]
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Construct JSON payload, serialize to UTF-8 bytes, and transmit over the socket
            response_data = {"msg": text}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
                
                
        else:
            self.send_response(404)
            self.end_headers()
    
# Instantiate server and run it
server = HTTPServer(('', PORT), MyReqHandler)
print("Server is listening on port 8080...")

# Blocking function: listening http requests from clients
server.serve_forever()
