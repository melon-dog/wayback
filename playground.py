import os
import time
from dotenv import load_dotenv
from src.wayback import WayBack, WayBackStatus, WayBackSave


def main():
    load_dotenv()
    confirmed = False

    def on_confirm(result: WayBackStatus):
        nonlocal confirmed
        print(result.status)
        confirmed = True

    wayback = WayBack(os.getenv("ARCHIVE_ACCESS"), os.getenv("ARCHIVE_SECRET"))
    saveResponse = wayback.save(
        "https://docs.python.org/3/",
        delay_wb_availability=1,
        on_confirmation=on_confirm,
    )

    print(saveResponse)
    print("Waiting for confirmation...")
    while not confirmed:
        time.sleep(1)


if __name__ == "__main__":
    main()
