import time

from googleapiclient.errors import HttpError

from compute import ComputeClient

compute = ComputeClient()


def handle_compute_instance(
    event: dict,
    registry,
):

    resource = event.get("resource", {})
    proto = event.get("protoPayload", {})

    project_id = resource.get("labels", {}).get("project_id")

    resource_name = proto.get("resourceName", "")
    parts = resource_name.split("/")

    zone = parts[parts.index("zones") + 1]
    instance_name = parts[parts.index("instances") + 1]

    print("=" * 80)
    print("COMPUTE HANDLER")
    print("=" * 80)
    print(f"Project ID : {project_id}")
    print(f"Zone       : {zone}")
    print(f"Instance   : {instance_name}")

    print("=" * 80)
    print("REGISTRY FOUND")
    print("=" * 80)
    print(f"Product      : {registry.product}")
    print(f"Team         : {registry.team}")
    print(f"Department   : {registry.department}")
    print(f"Owner        : {registry.owner}")
    print(f"Cost Centre  : {registry.cost_center}")

    #
    # Retry because Compute Engine may take a few seconds
    # before the VM becomes readable.
    #

    for attempt in range(10):

        try:

            existing_labels, fingerprint = compute.get_labels(
                project_id,
                zone,
                instance_name,
            )

            break

        except HttpError as e:

            if e.resp.status == 404:

                print(
                    f"Instance not found ({attempt + 1}/10)"
                )

                time.sleep(3)
                continue

            raise

    else:

        raise Exception(
            f"Instance '{instance_name}' never became available."
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
            "owner": registry.owner.lower()
            .replace("@", "-")
            .replace(".", "-"),
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

    return response