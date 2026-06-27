import json

from clients.storage import StorageClient

from config import (
    STORAGE_RETRY_COUNT,
    STORAGE_RETRY_SLEEP,
)

from utils.retry import retry_on_404
from utils.labels import build_labels
from utils.logger import banner, item

storage = StorageClient()


def handle_storage_bucket(
    event: dict,
    registry,
):

    banner("STORAGE HANDLER")

    print("=" * 80)
    print("RAW STORAGE EVENT")
    print("=" * 80)
    print(json.dumps(event, indent=2))

    proto = event.get("protoPayload", {})

    resource_name = proto.get(
        "resourceName",
        "",
    )

    print("=" * 80)
    print("RESOURCE NAME")
    print("=" * 80)
    print(resource_name)

    bucket_name = resource_name.split("/")[-1]

    print("=" * 80)
    print("PARSED BUCKET")
    print("=" * 80)
    print(bucket_name)

    banner("REGISTRY")

    item("Product", registry.product)
    item("Team", registry.team)
    item("Department", registry.department)
    item("Owner", registry.owner)
    item("Cost Centre", registry.cost_center)

    result = retry_on_404(
        lambda: storage.get_labels(
            bucket_name,
        ),
        retries=STORAGE_RETRY_COUNT,
        sleep=STORAGE_RETRY_SLEEP,
    )

    if result is None:

        banner("BUCKET NOT AVAILABLE")

        item("Bucket", bucket_name)

        return {
            "status": "SKIPPED",
            "bucket": bucket_name,
        }

    existing_labels, metageneration = result

    banner("EXISTING LABELS")
    print(existing_labels)

    new_labels = existing_labels.copy()
    new_labels.update(build_labels(registry))

    banner("NEW LABELS")
    print(new_labels)

    response = storage.set_labels(
        bucket_name,
        new_labels,
        metageneration,
    )

    banner("LABEL UPDATE RESPONSE")
    print(response)

    return response