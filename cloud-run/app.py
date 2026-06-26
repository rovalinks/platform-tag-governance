from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    print("=" * 80)
    print("RAW EVENT")
    print("=" * 80)
    print(json.dumps(event, indent=2))

    print("=" * 80)
    print("EVENT KEYS")
    print("=" * 80)
    print(event.keys())

    return "OK", 200