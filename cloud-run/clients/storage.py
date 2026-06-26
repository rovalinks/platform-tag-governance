from google.cloud import storage


class StorageClient:

    def __init__(self):
        self.client = storage.Client()

    def get_bucket(
        self,
        bucket_name: str,
    ):
        return self.client.bucket(bucket_name)

    def get_labels(
        self,
        bucket_name: str,
    ):

        bucket = self.get_bucket(bucket_name)

        bucket.reload()

        labels = bucket.labels or {}

        return labels

    def set_labels(
        self,
        bucket_name: str,
        labels: dict,
    ):

        bucket = self.get_bucket(bucket_name)

        bucket.reload()

        bucket.labels = labels

        bucket.patch()

        return {
            "bucket": bucket.name,
            "labels": bucket.labels,
            "status": "UPDATED",
        }