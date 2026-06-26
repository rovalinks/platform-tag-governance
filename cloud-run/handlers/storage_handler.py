from clients.storage import StorageClient

storage = StorageClient()


def handle_storage_bucket(
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

    #
    # resourceName format:
    #
    # projects/_/buckets/my-bucket
    #

    bucket_name = resource_name.split("/")[-1]

    print("=" * 80)
    print("STORAGE HANDLER")
    print("=" * 80)

    print(f"Project : {project_id}")
    print(f"Bucket  : {bucket_name}")

    existing_labels = storage.get_bucket_labels(
        bucket_name,
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

    response = storage.set_bucket_labels(
        bucket_name,
        new_labels,
    )

    print("=" * 80)
    print("LABEL UPDATE RESPONSE")
    print("=" * 80)
    print(response)

    return response