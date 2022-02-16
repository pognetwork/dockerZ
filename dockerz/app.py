import os
import threading

KEY = os.environ.get("DOCKERZKEY") if os.environ.get("DOCKERZKEY") else "someDefaultKey"
tasks = []
currentTask = None

def loop():
    while True:
        if len(tasks) and currentTask is None:
            currentTask = tasks.pop(0)
            
            # run the task
            # 1. start 2 or more containers based on the canary image
            # 2. run function on container 1 and test if it worked on container 2
            # 3. Profit
    
threading.Thread(target=loop)
