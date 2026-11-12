import asyncio
import hashlib
from quart import Quart, request, make_response
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = Quart(__name__)

# --- Qui definirai i tuoi endpoint @app.route() ---

async def main():
    config = Config()
    # Binding per il classico HTTPS su TCP
    config.bind = ["0.0.0.0:4433"]        
    # Binding per QUIC su UDP
    config.quic_bind = ["0.0.0.0:4433"]   
    
    # Percorsi dei certificati generati
    config.certfile = "cert.pem"
    config.keyfile = "key.pem"

    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())