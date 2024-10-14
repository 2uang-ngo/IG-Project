import os
import time
import datetime

# Path to the file to save the runtime
last_run_file = "your path"

# Last runtime check function
def can_run(hour=2):
    if os.path.exists(last_run_file):
        with open(last_run_file, 'r') as f:
            last_run_time = float(f.read().strip())
            if time.time() - last_run_time < hour*3600 :  # 5 hours
                return False
    return True

# Runtime storage function
def update_last_run():
    with open(last_run_file, 'w') as f:
        f.write(str(time.time()))
if __name__=="__main__":
    # Run scripts if possible
    if can_run():
        print("Script running....")
        os.chdir("your path")
        os.system("your python file")
        # Put your logic here
        update_last_run()
        time.sleep(10)
    else:
        print("Script has been running for the last 2 hours, not running again.")
        time.sleep(10)
