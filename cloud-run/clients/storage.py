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

    def get_bucket(self, bucket_name):

        return (
            self.storage.buckets()
            .get(bucket=bucket_name)
            .execute()
        )

    def get_labels(self, bucket_name):

        bucket = self.get_bucket(bucket_name)

        return (
            bucket.get("labels", {}),
            bucket["metageneration"],
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

        return (
            self.storage.buckets()
            .patch(
                bucket=bucket_name,
                body=body,
                ifMetagenerationMatch=metageneration,
            )
            .execute()
        )