import asyncio
import hashlib
from quart import Quart, request, make_response
from hypercorn.config import Config
from hypercorn.asyncio import serve
from hashlib import sha256

app = Quart(__name__)

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
    
@app.route('/', methods=['GET'])
async def get():
    version = request.http_version
    response = await make_response("Ok", 200)
    if version != "3":
        response.headers["Alt-Svc"] = 'h3=":4433"'
    return response

@app.route('/proto', methods=['GET'])
async def get_proto():
    version = request.http_version
    response = await make_response(f"HTTP/{version}", 200)
    return response

@app.route('/hash', methods=['POST'])
async def post_hash():
    body = await request.get_data()
    hashed_body = sha256(body)
    hex_body = hashed_body.hexdigest()
    response = await make_response(f"{hex_body}", 200)
    return response

if __name__ == "__main__":
    asyncio.run(main())