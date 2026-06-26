from handlers.compute_handler import handle_compute_instance
from handlers.storage_handler import handle_storage_bucket


class Dispatcher:

    def dispatch(
        self,
        event: dict,
        registry,
    ):

        resource = event.get("resource", {})
        resource_type = resource.get("type")

        print("=" * 80)
        print("DISPATCHER")
        print("=" * 80)
        print(f"Resource Type : {resource_type}")

        if resource_type == "gce_instance":
            return handle_compute_instance(
                event,
                registry,
            )

        elif resource_type == "gcs_bucket":
            return handle_storage_bucket(
                event,
                registry,
            )

        print(f"No handler implemented for '{resource_type}'")

        return "IGNORED"