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
        resource_type = resource.get("type")

        banner("DISPATCHER")

        item("Resource Type", resource_type)

        if resource_type == COMPUTE_INSTANCE:

            return handle_compute_instance(
                event,
                registry,
            )

        elif resource_type == STORAGE_BUCKET:

            return handle_storage_bucket(
                event,
                registry,
            )

        banner("NO HANDLER")

        item("Resource Type", resource_type)

        return {
            "status": "IGNORED",
            "resource_type": resource_type,
        }