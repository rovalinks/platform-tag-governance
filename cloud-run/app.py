from flask import Flask, request
import json
import time

from googleapiclient.errors import HttpError

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

    #
    # Ignore the first Audit Log event.
    # Only process the final event once the operation has completed.
    #
    operation = data.get("operation", {})

    if not operation.get("last", False):
        print("=" * 80)
        print("Ignoring operation.first event")
        print("=" * 80)
        return "OK", 200

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

    #
    # Wait until the VM becomes readable.
    #
    existing_labels = None
    fingerprint = None

    for attempt in range(10):

        try:

            existing_labels, fingerprint = compute.get_labels(
                project_id,
                zone,
                instance_name,
            )

            print(f"Instance became available after {attempt + 1} attempt(s).")
            break

        except HttpError as e:

            #
            # VM not yet visible or already deleted.
            #
            if e.resp.status == 404:

                print(
                    f"Instance not ready ({attempt + 1}/10). Waiting..."
                )

                time.sleep(3)
                continue

            raise

    #
    # If the VM never appeared, acknowledge the event.
    # This prevents Eventarc from retrying forever.
    #
    if existing_labels is None:

        print("=" * 80)
        print("INSTANCE NOT FOUND")
        print("=" * 80)
        print(f"{instance_name} no longer exists.")
        print("Acknowledging Eventarc event.")
        print("=" * 80)

        return "OK", 200

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