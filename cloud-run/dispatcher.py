from handlers.compute_handler import handle_compute_instance
from handlers.disk_handler import handle_compute_disk
from handlers.snapshot_handler import handle_compute_snapshot
# from handlers.image_handler import handle_compute_image
# from handlers.address_handler import handle_compute_address
# from handlers.instance_template_handler import handle_compute_instance_template
# from handlers.machine_image_handler import handle_compute_machine_image
from handlers.storage_handler import handle_storage_bucket

from utils.constants import (
    COMPUTE_INSTANCE,
    COMPUTE_DISK,
    COMPUTE_SNAPSHOT,
    STORAGE_BUCKET,
)

from utils.logger import banner, item


class Dispatcher:

    def dispatch(
        self,
        event: dict,
        registry,
    ):

        resource = event.get(
            "resource",
            {},
        )

        resource_type = resource.get(
            "type",
        )

        banner("DISPATCHER")

        item(
            "Resource Type",
            resource_type,
        )

        if resource_type == COMPUTE_INSTANCE:
            return handle_compute_instance(event, registry)

        elif resource_type == COMPUTE_DISK:
            return handle_compute_disk(event, registry)

        elif resource_type == COMPUTE_SNAPSHOT:
            return handle_compute_snapshot(event, registry)

        # elif resource_type == COMPUTE_IMAGE:
        #     return handle_compute_image(event, registry)

        # elif resource_type == COMPUTE_ADDRESS:
        #     return handle_compute_address(event, registry)

        # elif resource_type == COMPUTE_INSTANCE_TEMPLATE:
        #     return handle_compute_instance_template(event, registry)

        # elif resource_type == COMPUTE_MACHINE_IMAGE:
        #     return handle_compute_machine_image(event, registry)

        elif resource_type == STORAGE_BUCKET:
            return handle_storage_bucket(event, registry)

        banner("NO HANDLER")

        item(
            "Resource Type",
            resource_type,
        )

        return {
            "status": "IGNORED",
            "resource_type": resource_type,
        }