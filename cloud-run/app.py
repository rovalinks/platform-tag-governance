from flask import Flask, request
import inspect

from registry import RegistryReader
from models import Registry

app = Flask(__name__)

reader = RegistryReader()


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/debug", methods=["GET"])
def debug():

    return {
        "registry_signature": str(inspect.signature(Registry)),
        "registry_annotations": Registry.__annotations__,
    }


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    data = event.get("data", event)
    resource = data.get("resource", {})

    project_id = resource.get("labels", {}).get("project_id")

    registry = reader.find_by_project(project_id)

    print("=" * 80)
    print("REGISTRY FOUND")
    print("=" * 80)
    print(f"Product      : {registry.product}")
    print(f"Team         : {registry.team}")
    print(f"Department   : {registry.department}")
    print(f"Owner        : {registry.owner}")
    print(f"Cost Centre  : {registry.cost_center}")
    print("=" * 80)

    return "OK", 200