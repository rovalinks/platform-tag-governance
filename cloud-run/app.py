from flask import Flask, request
import json

from registry import RegistryReader

app = Flask(__name__)

reader = RegistryReader()


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

    # Eventarc sends the Audit Log inside "data"
    data = event.get("data", event)

    resource = data.get("resource", {})
    proto = data.get("protoPayload", {})

    project_id = resource.get("labels", {}).get("project_id")

    resource_name = proto.get("resourceName", "")

    # Example:
    # projects/my-project/zones/europe-west2-a/instances/test-vm

    parts = resource_name.split("/")

    zone = None
    instance_name = None

    if "zones" in parts:
        zone = parts[parts.index("zones") + 1]

    if "instances" in parts:
        instance_name = parts[parts.index("instances") + 1]

    print("=" * 80)
    print("EVENT DETAILS")
    print("=" * 80)
    print(f"Project ID   : {project_id}")
    print(f"Zone         : {zone}")
    print(f"Instance     : {instance_name}")
    print("=" * 80)

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