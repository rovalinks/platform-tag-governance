import time

from googleapiclient.errors import HttpError


def retry_on_404(function, retries, sleep):

    for attempt in range(retries):

        try:
            return function()

        except HttpError as e:

            if e.resp.status == 404:

                print(
                    f"Resource not ready ({attempt + 1}/{retries})"
                )

                time.sleep(sleep)
                continue

            raise

    return None