from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200

@app.route("/", methods=["POST"])
def receive_event():
    print(json.dumps(request.json, indent=2))
    return "OK", 200