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
    print("STEP 1 - RAW STORAGE EVENT")
    print("=" * 80)
    print(json.dumps(event, indent=2))

    print("=" * 80)
    print("STEP 2 - GET protoPayload")
    print("=" * 80)

    proto = event.get("protoPayload", {})

    print(proto)

    print("=" * 80)
    print("STEP 3 - GET resourceName")
    print("=" * 80)

    resource_name = proto.get(
        "resourceName",
        "",
    )

    print(resource_name)

    print("=" * 80)
    print("STEP 4 - PARSE BUCKET")
    print("=" * 80)

    bucket_name = resource_name.split("/")[-1]

    print(bucket_name)

    banner("REGISTRY")

    item("Product", registry.product)
    item("Team", registry.team)
    item("Department", registry.department)
    item("Owner", registry.owner)
    item("Cost Centre", registry.cost_center)

    print("=" * 80)
    print("STEP 5 - GET EXISTING LABELS")
    print("=" * 80)

    result = retry_on_404(
        lambda: storage.get_labels(
            bucket_name,
        ),
        retries=STORAGE_RETRY_COUNT,
        sleep=STORAGE_RETRY_SLEEP,
    )

    print("Retry Result:")
    print(result)

    if result is None:

        banner("BUCKET NOT AVAILABLE")

        item("Bucket", bucket_name)

        return {
            "status": "SKIPPED",
            "bucket": bucket_name,
        }

    existing_labels, metageneration = result

    print("=" * 80)
    print("STEP 6 - EXISTING LABELS")
    print("=" * 80)
    print(existing_labels)

    print("=" * 80)
    print("STEP 7 - BUILD LABELS")
    print("=" * 80)

    new_labels = existing_labels.copy()
    new_labels.update(
        build_labels(
            registry,
        )
    )

    print(new_labels)

    print("=" * 80)
    print("STEP 8 - PATCH BUCKET")
    print("=" * 80)

    response = storage.set_labels(
        bucket_name,
        new_labels,
        metageneration,
    )

    print("=" * 80)
    print("STEP 9 - PATCH RESPONSE")
    print("=" * 80)
    print(response)

    return response