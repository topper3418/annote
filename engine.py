import time
from src.engine import associate_entry


def run_scheduler():
    try:
        while True:
            associate_entry()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

if __name__ == "__main__":
    run_scheduler()
