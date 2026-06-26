from flask import Flask, request

from registry import RegistryReader
from dispatcher import Dispatcher

app = Flask(__name__)

reader = RegistryReader()
dispatcher = Dispatcher()

DEBUG = False


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    print("=" * 80)
    print("EVENT RECEIVED")
    print("=" * 80)

    if DEBUG:
        import json
        print(json.dumps(event, indent=2))

    data = event.get("data", event)

    #
    # Ignore the first Audit Log event.
    # Process only once the operation has completed.
    #
    operation = data.get("operation", {})

    if not operation.get("last", False):

        print("=" * 80)
        print("Ignoring operation.first event")
        print("=" * 80)

        return "OK", 200

    resource = data.get("resource", {})

    project_id = resource.get(
        "labels",
        {},
    ).get(
        "project_id",
    )

    print("=" * 80)
    print("PROJECT")
    print("=" * 80)
    print(f"Project ID : {project_id}")

    registry = reader.find_by_project(project_id)

    dispatcher.dispatch(
        data,
        registry,
    )

    return "OK", 200