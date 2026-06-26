from clients.compute import ComputeClient

from config import (
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
)

from utils.retry import retry_on_404
from utils.labels import build_labels
from utils.logger import banner, item

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

    banner("COMPUTE HANDLER")

    item("Project", project_id)
    item("Zone", zone)
    item("Instance", instance_name)

    banner("REGISTRY")

    item("Product", registry.product)
    item("Team", registry.team)
    item("Department", registry.department)
    item("Owner", registry.owner)
    item("Cost Centre", registry.cost_center)

    result = retry_on_404(
        lambda: compute.get_labels(
            project_id,
            zone,
            instance_name,
        ),
        retries=MAX_RETRIES,
        sleep=RETRY_DELAY_SECONDS,
    )

    if result is None:

        banner("INSTANCE NOT AVAILABLE")

        item("Instance", instance_name)

        return {
            "status": "SKIPPED",
            "reason": "Instance not found after retries",
            "instance": instance_name,
        }

    existing_labels, fingerprint = result

    banner("EXISTING LABELS")
    print(existing_labels)

    new_labels = existing_labels.copy()
    new_labels.update(build_labels(registry))

    banner("NEW LABELS")
    print(new_labels)

    response = compute.set_labels(
        project_id,
        zone,
        instance_name,
        new_labels,
        fingerprint,
    )

    banner("LABEL UPDATE RESPONSE")
    print(response)

    return response