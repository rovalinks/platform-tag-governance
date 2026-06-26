from flask import Flask, request
import json

from registry import RegistryReader
from compute import ComputeClient

app = Flask(__name__)

reader = RegistryReader()
compute = ComputeClient()


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

    data = event.get("data", event)

    resource = data.get("resource", {})
    proto = data.get("protoPayload", {})

    project_id = resource.get("labels", {}).get("project_id")

    resource_name = proto.get("resourceName", "")
    parts = resource_name.split("/")

    zone = parts[parts.index("zones") + 1]
    instance_name = parts[parts.index("instances") + 1]

    print("=" * 80)
    print("EVENT DETAILS")
    print("=" * 80)
    print(f"Project ID : {project_id}")
    print(f"Zone       : {zone}")
    print(f"Instance   : {instance_name}")

    registry = reader.find_by_project(project_id)

    print("=" * 80)
    print("REGISTRY FOUND")
    print("=" * 80)
    print(f"Product      : {registry.product}")
    print(f"Team         : {registry.team}")
    print(f"Department   : {registry.department}")
    print(f"Owner        : {registry.owner}")
    print(f"Cost Centre  : {registry.cost_center}")

    existing_labels, fingerprint = compute.get_labels(
        project_id,
        zone,
        instance_name,
    )

    print("=" * 80)
    print("EXISTING LABELS")
    print("=" * 80)
    print(existing_labels)

    new_labels = existing_labels.copy()

    new_labels.update(
        {
            "product": registry.product.lower(),
            "team": registry.team.lower(),
            "department": registry.department.lower(),
            "owner": registry.owner.lower().replace("@", "-").replace(".", "-"),
            "costcentre": registry.cost_center.lower(),
        }
    )

    print("=" * 80)
    print("NEW LABELS")
    print("=" * 80)
    print(new_labels)

    response = compute.set_labels(
        project_id,
        zone,
        instance_name,
        new_labels,
        fingerprint,
    )

    print("=" * 80)
    print("LABEL UPDATE RESPONSE")
    print("=" * 80)
    print(response)

    return "OK", 200