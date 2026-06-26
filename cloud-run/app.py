from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


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

    logging.info("========== EVENT RECEIVED ==========")
    logging.info("Project      : %s", project_id)
    logging.info("Zone         : %s", zone)
    logging.info("Resource     : %s", resource_name)
    logging.info("Created By   : %s", principal)

    return "OK", 200