from google.auth import default
from googleapiclient.discovery import build


class StorageClient:

    def __init__(self):

        credentials, _ = default()

        self.storage = build(
            "storage",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

    def get_bucket(
        self,
        bucket_name,
    ):

        print("=" * 80)
        print("GET BUCKET")
        print("=" * 80)
        print(bucket_name)

        print("=" * 80)
        print("ABOUT TO CALL STORAGE API")
        print("=" * 80)

        response = (
            self.storage.buckets()
            .get(
                bucket=bucket_name,
            )
            .execute()
        )

        print("=" * 80)
        print("GET BUCKET RESPONSE")
        print("=" * 80)
        print(response)

        return response

    def get_labels(
        self,
        bucket_name,
    ):

        bucket = self.get_bucket(
            bucket_name,
        )

        labels = bucket.get(
            "labels",
            {},
        )

        metageneration = bucket[
            "metageneration"
        ]

        print("=" * 80)
        print("CURRENT LABELS")
        print("=" * 80)
        print(labels)

        print("=" * 80)
        print("METAGENERATION")
        print("=" * 80)
        print(metageneration)

        return (
            labels,
            metageneration,
        )

    def set_labels(
        self,
        bucket_name,
        labels,
        metageneration,
    ):

        body = {
            "labels": labels,
        }

        print("=" * 80)
        print("PATCH REQUEST")
        print("=" * 80)
        print(f"Bucket          : {bucket_name}")
        print(f"Labels          : {labels}")
        print(f"Metageneration  : {metageneration}")

        response = (
            self.storage.buckets()
            .patch(
                bucket=bucket_name,
                body=body,
                ifMetagenerationMatch=metageneration,
            )
            .execute()
        )

        print("=" * 80)
        print("PATCH RESPONSE")
        print("=" * 80)
        print(response)

        return response