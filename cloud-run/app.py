from flask import Flask, request
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    logging.info("########################################")
    logging.info("NEW VERSION OF APP.PY IS RUNNING")
    logging.info("########################################")

    logging.info(json.dumps(event, indent=2))

    return "OK", 200