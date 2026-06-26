from handlers.compute_handler import handle_compute_instance


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

        print(f"No handler implemented for '{resource_type}'")

        return "IGNORED"