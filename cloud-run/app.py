from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    return "Healthy", 200


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    proto = event.get("protoPayload", {})
    resource = event.get("resource", {})

    project_id = resource.get("labels", {}).get("project_id")
    zone = resource.get("labels", {}).get("zone")
    resource_name = proto.get("resourceName")
    principal = proto.get("authenticationInfo", {}).get("principalEmail")

    print("=" * 80)
    print("EVENT SUMMARY")
    print("=" * 80)

    print(f"Project      : {project_id}")
    print(f"Zone         : {zone}")
    print(f"Resource     : {resource_name}")
    print(f"Created By   : {principal}")

    print("=" * 80)

    return "OK", 200