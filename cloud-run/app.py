from flask import Flask
import inspect

from models import Registry

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/debug")
def debug():

    import inspect

    return {
        "signature": str(inspect.signature(Registry)),
        "annotations": {
            k: str(v)
            for k, v in Registry.__annotations__.items()
        }
    }