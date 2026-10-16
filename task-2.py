# HTTP: mini API
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

PORT = 8080

# Subclass of BaseHTTPRequestHandler
class MyReqHandler(BaseHTTPRequestHandler):
    
    # Database to save notes through POST request
    _notes_db = {}
    _next_note_id = 1    # Auto-incrementing primary key
    
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
        
        
    # Modify do_POST method to have desired behaviour
    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        
        if path != '/notes':
            self.send_response(404)
            self.end_headers()
            return
        
        else:
            content_type = self.headers.get('Content-Type')
            if content_type != 'application/json':
                self.send_response(415)
                self.end_headers()
                return
            
            # Read the payload size from headers
            content_length = int(self.headers.get('Content-Length', 0))
            body_bytes = self.rfile.read(content_length)
            
            # Parse JSON inside a try-except block:
            try:
                data = json.loads(body_bytes.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_response(400)
                self.end_headers()
                return
                # Return 400 Bad Request
            
            # Validation check:
            if not isinstance(data, dict) or 'text' not in data or not isinstance(data['text'], str):
                self.send_response(400)
                self.end_headers()
                return
            
        
        
        note_id = MyReqHandler._next_note_id
        MyReqHandler._notes_db[note_id] = data['text']
            
    

    
# Instantiate server and run it
server = HTTPServer(('', PORT), MyReqHandler)
print("Server is listening on port 8080...")

# Blocking function: listening http requests from clients
server.serve_forever()
