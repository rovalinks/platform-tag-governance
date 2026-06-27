from google.auth import default
from googleapiclient.discovery import build


class SnapshotClient:

    def __init__(self):

        credentials, _ = default()

        self.compute = build(
            "compute",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

    def get_snapshot(
        self,
        project_id,
        snapshot_name,
    ):

        return (
            self.compute.snapshots()
            .get(
                project=project_id,
                snapshot=snapshot_name,
            )
            .execute()
        )

    def get_labels(
        self,
        project_id,
        snapshot_name,
    ):

        snapshot = self.get_snapshot(
            project_id,
            snapshot_name,
        )

        return (
            snapshot.get("labels", {}),
            snapshot["labelFingerprint"],
        )

    def set_labels(
        self,
        project_id,
        snapshot_name,
        labels,
        fingerprint,
    ):

        body = {
            "labels": labels,
            "labelFingerprint": fingerprint,
        }

        return (
            self.compute.snapshots()
            .setLabels(
                project=project_id,
                resource=snapshot_name,
                body=body,
            )
            .execute()
        )