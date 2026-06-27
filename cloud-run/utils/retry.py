import time

from googleapiclient.errors import HttpError


def retry_on_404(
    function,
    retries,
    sleep,
):

    for attempt in range(retries):

        try:

            return function()

        except HttpError as e:

            print("=" * 80)
            print("HTTP ERROR")
            print("=" * 80)
            print(f"Status : {e.resp.status}")

            try:
                print(e.content.decode())
            except Exception:
                print(e)

            if e.resp.status == 404:

                print(
                    f"Resource not ready ({attempt + 1}/{retries})"
                )

                time.sleep(sleep)
                continue

            raise

        except Exception as e:

            print("=" * 80)
            print("UNEXPECTED ERROR")
            print("=" * 80)
            print(type(e).__name__)
            print(str(e))

            raise

    print("=" * 80)
    print("RETRY FAILED")
    print("=" * 80)
    print("Maximum retries exceeded")

    return None