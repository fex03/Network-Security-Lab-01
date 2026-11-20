from flask import Flask, request, make_response, abort, jsonify

PORT = 8090

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>OK</p>"

        

if (__name__=='__main__'):
    app.run(host='0.0.0.0', port=PORT)
