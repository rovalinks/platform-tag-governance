from google.cloud import storage


class StorageClient:

    def __init__(self):

        self.client = storage.Client()

    def get_bucket_labels(
        self,
        bucket_name,
    ):

        bucket = self.client.bucket(bucket_name)
        bucket.reload()

        return bucket.labels

    def set_bucket_labels(
        self,
        bucket_name,
        labels,
    ):

        bucket = self.client.bucket(bucket_name)

        bucket.reload()

        bucket.labels = labels

        bucket.patch()

        return {
            "status": "SUCCESS",
            "bucket": bucket_name,
        }