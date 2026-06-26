from flask import Flask
import inspect

from models import Registry

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/debug", methods=["GET"])
def debug():

    return {
        "signature": str(inspect.signature(Registry)),
        "annotations": Registry.__annotations__
    }