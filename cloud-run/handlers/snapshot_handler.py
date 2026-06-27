from clients.snapshot import SnapshotClient

from config import (
    COMPUTE_RETRY_COUNT,
    COMPUTE_RETRY_SLEEP,
)

from utils.retry import retry_on_404
from utils.labels import build_labels
from utils.logger import banner, item

snapshot = SnapshotClient()


def handle_compute_snapshot(
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

    snapshot_name = resource_name.split("/")[-1]

    banner("COMPUTE SNAPSHOT HANDLER")

    item("Project", project_id)
    item("Snapshot", snapshot_name)

    banner("REGISTRY")

    item("Product", registry.product)
    item("Team", registry.team)
    item("Department", registry.department)
    item("Owner", registry.owner)
    item("Cost Centre", registry.cost_center)

    result = retry_on_404(
        lambda: snapshot.get_labels(
            project_id,
            snapshot_name,
        ),
        retries=COMPUTE_RETRY_COUNT,
        sleep=COMPUTE_RETRY_SLEEP,
    )

    if result is None:

        banner("SNAPSHOT NOT AVAILABLE")

        item("Snapshot", snapshot_name)

        return {
            "status": "SKIPPED",
            "reason": "Snapshot not found after retries",
            "snapshot": snapshot_name,
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

    response = snapshot.set_labels(
        project_id,
        snapshot_name,
        new_labels,
        fingerprint,
    )

    banner("LABEL UPDATE RESPONSE")
    print(response)

    return response