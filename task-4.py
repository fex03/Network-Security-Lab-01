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

