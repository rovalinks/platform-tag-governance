from handlers.compute_handler import handle_compute_instance
from handlers.bucket_handler import handle_bucket


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
        print(f"Resource Type    : {resource_type}")

        #
        # Compute Engine
        #
        if resource_type == "gce_instance":

            print("Selected Handler : Compute")

            return handle_compute_instance(
                event,
                registry,
            )

        #
        # Cloud Storage
        #
        elif resource_type == "gcs_bucket":

            print("Selected Handler : Cloud Storage")

            return handle_bucket(
                event,
                registry,
            )

        #
        # Unsupported resource
        #
        print("Selected Handler : None")
        print(f"No handler implemented for '{resource_type}'")

        return "IGNORED"