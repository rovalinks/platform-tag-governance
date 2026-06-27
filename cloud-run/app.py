from flask import Flask
from flask import request

from dispatcher import Dispatcher
from registry import RegistryReader

from utils.logger import (
    banner,
    item,
)

app = Flask(__name__)

reader = RegistryReader()
dispatcher = Dispatcher()

DEBUG = False


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    banner("EVENT RECEIVED")

    import json

    print("=" * 80)
    print("FULL EVENT")
    print("=" * 80)
    print(json.dumps(event, indent=2))

    data = event.get(
        "data",
        event,
    )

    print("=" * 80)
    print("DATA")
    print("=" * 80)
    print(json.dumps(data, indent=2))

    operation = data.get(
        "operation",
        {},
    )

    if not operation.get(
        "last",
        False,
    ):

        banner("IGNORING FIRST EVENT")

        return "OK", 200

    resource = data.get(
        "resource",
        {},
    )

    project_id = resource.get(
        "labels",
        {},
    ).get(
        "project_id",
    )

    banner("PROJECT")

    item("Project ID", project_id)

    registry = reader.find_by_project(
        project_id
    )

    response = dispatcher.dispatch(
        data,
        registry,
    )

    banner("HANDLER RESPONSE")

    print(response)

    return "OK", 200