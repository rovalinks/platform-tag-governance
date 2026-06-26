from registry import RegistryReader

reader = RegistryReader()


@app.route("/", methods=["POST"])
def receive_event():

    event = request.get_json()

    data = event.get("data", event)

    proto = data.get("protoPayload", {})
    resource = data.get("resource", {})

    project_id = resource.get("labels", {}).get("project_id")

    registry = reader.find_by_project(project_id)

    print("=" * 80)
    print(f"Application : {registry.application}")
    print(f"Department  : {registry.department}")
    print(f"Owner       : {registry.owner}")
    print(f"Cost Centre : {registry.cost_center}")
    print("=" * 80)

    return "OK", 200