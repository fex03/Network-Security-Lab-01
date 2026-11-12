import asyncio
import os
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import HeadersReceived, DataReceived
from aioquic.quic.configuration import QuicConfiguration

PORT1 = 4433

# Configuration for our QUIC server
configuration = QuicConfiguration(
    is_client=False,
    # Standard ports for certs we just made
    certificate_path='server.crt',
    private_key_path='server.key',
)

class Http3Handler(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Each connection gets its own H3 instance
        self._h3 = H3Connection(self._quic)
 
    def quic_event_received(self, event):
        # A standard QUIC event (like packet received)
        # We pass it to the H3 state machine
        for h3_event in self._h3.handle_event(event):
            if isinstance(h3_event, HeadersReceived):
                self._handle_request(h3_event.stream_id, h3_event.headers)
 
    def _handle_request(self, stream_id, headers):
        # Extract the path from headers
        # Headers are a list of tuples: [(b':method', b'GET'), (b':path', b'/')...]
        headers_dict = {k: v for k, v in headers}
        path = headers_dict.get(b':path', b'/').decode()
 
        print(f'[+] Client requested: {path}')
 
        # Prepare the response body
        response_body = f'Welcome to HTTP/3! You asked for {path}'.encode()
 
        # 1. Send Response Headers (Status 200 OK)
        self._h3.send_headers(
            stream_id=stream_id,
            headers=[
                (b':status', b'200'),
                (b'server', b'python-aioquic-example'),
                (b'content-type', b'text/plain'),
                (b'content-length', str(len(response_body)).encode()),
            ],
        )
 
        # 2. Send Response DATA
        self._h3.send_data(stream_id=stream_id, data=response_body, end_stream=True)
 
        # 3. Flush packets to the network
        self.transmit()
        
        