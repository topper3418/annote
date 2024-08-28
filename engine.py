import time

def cycle_engine():
    """Function to be run every second."""
    # check the max processed entry id versus the max entry id
    # if they match, exit
    # if they don't, prompt the AI
    # get the current focus scope, pass it in along with the entry
    # ask it to generate tasks if applicable
    # ask it to generate actions to the existing tasks if applicable
    print("I'm running!")

def run_scheduler():
    try:
        while True:
            cycle_engine()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

if __name__ == "__main__":
    run_scheduler()
