import os
import threading
from flask import Flask, request
import Task

KEY = os.environ.get("DOCKERZKEY") if os.environ.get("DOCKERZKEY") else "someDefaultKey"
tasks = []
currentTask = None

http = Flask(__name__)
@http.route('/update/<key>', methods=['POST'])
def update(key):
    if key != KEY: return "invalid key", 401

    image = request.form.get("image", default="ghcr.io/pognetwork/champ")
    tag = request.form.get("tag", default="canary")
    commit = request.form.get("commit")

    tasks.append(Task(image, tag, commit))

    return 'Received!'

def loop():
    while True:
        if len(tasks) and currentTask is None:
            currentTask = tasks.pop(0)
            
            # run the task
            # 1. start 2 or more containers based on the canary image
            # 2. run function on container 1 and test if it worked on container 2
            # 3. Profit
    
threading.Thread(target=loop)
