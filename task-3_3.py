from flask import Flask, request
from ssl import create_default_context, Purpose, VerifyMode, CERT_REQUIRED

PORT = 8444

app = Flask(__name__)

ctx = create_default_context(purpose=Purpose.CLIENT_AUTH, cafile= "ca.crt")
ctx.verify_mode = CERT_REQUIRED
ctx.load_cert_chain('server.crt', 'server.key')


@app.route("/whoami", methods=['GET'])
def whoami():
    sock = request.environ['wsgi.input'].raw._sock
    cert = sock.getpeercert()
    common_name = None

    for item in cert.get('subject', ()):
        for key, value in item:
            if key == 'commonName':
                common_name = value
                break
            
    return common_name        

if (__name__=='__main__'):
    app.run(host='0.0.0.0', port=PORT, ssl_context=ctx)