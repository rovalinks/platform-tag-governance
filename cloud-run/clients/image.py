from google.auth import default
from googleapiclient.discovery import build


class ImageClient:

    def __init__(self):

        credentials, _ = default()

        self.compute = build(
            "compute",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

    def get_image(
        self,
        project_id,
        image_name,
    ):

        return (
            self.compute.images()
            .get(
                project=project_id,
                image=image_name,
            )
            .execute()
        )

    def get_labels(
        self,
        project_id,
        image_name,
    ):

        image = self.get_image(
            project_id,
            image_name,
        )

        return (
            image.get("labels", {}),
            image["labelFingerprint"],
        )

    def set_labels(
        self,
        project_id,
        image_name,
        labels,
        fingerprint,
    ):

        body = {
            "labels": labels,
            "labelFingerprint": fingerprint,
        }

        return (
            self.compute.images()
            .setLabels(
                project=project_id,
                resource=image_name,
                body=body,
            )
            .execute()
        )