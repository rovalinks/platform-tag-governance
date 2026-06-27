from handlers.compute_handler import handle_compute_instance
from handlers.storage_handler import handle_storage_bucket

from utils.constants import (
    COMPUTE_INSTANCE,
    STORAGE_BUCKET,
)

from utils.logger import banner, item


class Dispatcher:

    def dispatch(
        self,
        event: dict,
        registry,
    ):

        resource = event.get("resource", {})
        proto = event.get("protoPayload", {})

        banner("DISPATCHER DEBUG")

        print(resource)

        item("Resource Type", resource.get("type"))
        item("Service", proto.get("serviceName"))
        item("Method", proto.get("methodName"))

        #
        # TEMPORARY
        #
        print(">>> CALLING STORAGE HANDLER <<<")

        return handle_storage_bucket(
            event,
            registry,
        )