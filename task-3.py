from flask import Flask, request, make_response, abort, jsonify
from ssl import create_default_context, Purpose, CERT_REQUIRED

PORT = 8443

app = Flask(__name__)


ctx = create_default_context(purpose=Purpose.CLIENT_AUTH, cafile= "ca.crt")
ctx.verify_mode = CERT_REQUIRED
ctx.load_cert_chain('server.crt', 'server.key')

@app.route("/")
def hello_world():
    return "<p>OK</p>"

@app.route('/login', methods=['POST'])
def login():
    
    login = request.get_json()

    if login == None or login.get('user') == None:
        abort(401)
        
    if login.get('password') == "netsec":
        resp = make_response(jsonify({"message": "OK"}), 200)
        resp.set_cookie(key='session', value=login.get('user'), secure=True, httponly=True)
        return resp
    else:
        abort(401)
        
            
@app.route('/me', methods=['GET'])
def me():
    user = request.cookies.get('session')
    if user == None:
        abort(401)
    else:
        resp = make_response(jsonify({"user" : user}), 200)
        return resp
    

            

if (__name__=='__main__'):
    app.run(host='0.0.0.0', port=PORT, ssl_context=('server.crt', 'server.key'))