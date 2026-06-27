from clients.disk import DiskClient

from config import (
    COMPUTE_RETRY_COUNT,
    COMPUTE_RETRY_SLEEP,
)

from utils.retry import retry_on_404
from utils.labels import build_labels
from utils.logger import banner, item

disk = DiskClient()


def handle_compute_disk(
    event: dict,
    registry,
):

    resource = event.get("resource", {})
    proto = event.get("protoPayload", {})

    project_id = resource.get(
        "labels",
        {},
    ).get(
        "project_id",
    )

    resource_name = proto.get(
        "resourceName",
        "",
    )

    parts = resource_name.split("/")

    zone = parts[
        parts.index("zones") + 1
    ]

    disk_name = parts[
        parts.index("disks") + 1
    ]

    banner("COMPUTE DISK HANDLER")

    item("Project", project_id)
    item("Zone", zone)
    item("Disk", disk_name)

    banner("REGISTRY")

    item("Product", registry.product)
    item("Team", registry.team)
    item("Department", registry.department)
    item("Owner", registry.owner)
    item("Cost Centre", registry.cost_center)

    result = retry_on_404(
        lambda: disk.get_disk_labels(
            project_id,
            zone,
            disk_name,
        ),
        retries=COMPUTE_RETRY_COUNT,
        sleep=COMPUTE_RETRY_SLEEP,
    )

    if result is None:

        banner("DISK NOT AVAILABLE")

        item("Disk", disk_name)

        return {
            "status": "SKIPPED",
            "reason": "Disk not found after retries",
            "disk": disk_name,
        }

    existing_labels, fingerprint = result

    banner("EXISTING LABELS")
    print(existing_labels)

    new_labels = existing_labels.copy()
    new_labels.update(
        build_labels(registry)
    )

    banner("NEW LABELS")
    print(new_labels)

    response = disk.set_disk_labels(
        project_id,
        zone,
        disk_name,
        new_labels,
        fingerprint,
    )

    banner("LABEL UPDATE RESPONSE")
    print(response)

    return response