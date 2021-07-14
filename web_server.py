import bridge
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def root():
    app.do_teardown_appcontext()
    token = request.args.get("oauth_token")
    verifier = request.args.get("oauth_verifier")
    bridge.bridge([token,verifier])
    return "Done!"

def run_server():
    app.run(debug=False, port=8000)