from google.auth import default
from googleapiclient.discovery import build


class DiskClient:

    def __init__(self):

        credentials, _ = default()

        self.compute = build(
            "compute",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

    def get_disk(
        self,
        project_id,
        zone,
        disk_name,
    ):

        return (
            self.compute.disks()
            .get(
                project=project_id,
                zone=zone,
                disk=disk_name,
            )
            .execute()
        )

    def get_disk_labels(
        self,
        project_id,
        zone,
        disk_name,
    ):

        disk = self.get_disk(
            project_id,
            zone,
            disk_name,
        )

        return (
            disk.get("labels", {}),
            disk["labelFingerprint"],
        )

    def set_disk_labels(
        self,
        project_id,
        zone,
        disk_name,
        labels,
        fingerprint,
    ):

        body = {
            "labels": labels,
            "labelFingerprint": fingerprint,
        }

        return (
            self.compute.disks()
            .setLabels(
                project=project_id,
                zone=zone,
                resource=disk_name,
                body=body,
            )
            .execute()
        )