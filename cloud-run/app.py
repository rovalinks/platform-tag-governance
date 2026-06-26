from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/debug", methods=["GET"])
def debug():
    return {
        "status": "working"
    }