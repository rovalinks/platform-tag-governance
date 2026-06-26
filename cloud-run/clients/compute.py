from google.auth import default
from googleapiclient.discovery import build


class ComputeClient:

    def __init__(self):

        credentials, _ = default()

        self.compute = build(
            "compute",
            "v1",
            credentials=credentials,
            cache_discovery=False,
        )

    def get_instance(self, project_id, zone, instance_name):

        return self.compute.instances().get(
            project=project_id,
            zone=zone,
            instance=instance_name,
        ).execute()

    def get_labels(self, project_id, zone, instance_name):

        instance = self.get_instance(
            project_id,
            zone,
            instance_name,
        )

        return (
            instance.get("labels", {}),
            instance["labelFingerprint"],
        )

    def set_labels(
        self,
        project_id,
        zone,
        instance_name,
        labels,
        fingerprint,
    ):

        body = {
            "labels": labels,
            "labelFingerprint": fingerprint,
        }

        return (
            self.compute.instances()
            .setLabels(
                project=project_id,
                zone=zone,
                instance=instance_name,
                body=body,
            )
            .execute()
        )