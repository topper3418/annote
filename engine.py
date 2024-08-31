import time
from src.engine import process_entry


def run_scheduler():
    try:
        while True:
            process_entry()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

if __name__ == "__main__":
    run_scheduler()
