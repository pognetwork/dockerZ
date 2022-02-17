import os, threading
from flask import Flask, request
from task import Task
from multiprocessing import Process
from queue import Queue

DOCKERZ_KEY = os.environ.get("DOCKERZ_KEY", "someDefaultKey")
DOCKERZ_NETWORK = os.environ.get("DOCKERZ_NAME", "pog.network")
DOCKERZ_NROFNODES = int(os.environ.get("DOCKERZ_NROFNODES", "2"))

tasks = Queue()
currentTask = None

http = Flask(__name__)

@http.route('/update/<key>', methods=['POST'])
def update(key):
    if key != DOCKERZ_KEY: return "invalid key", 401
    print("route reached")

    image = request.form.get("image", default="ghcr.io/pognetwork/champ")
    tag = request.form.get("tag", default="canary")
    commit = request.form.get("commit")

    tasks.put(Task(image, tag, commit))
    return str(tasks.qsize())

def loop():
    while True:
        currentTask = tasks.get()
        currentTask.run(DOCKERZ_NETWORK, DOCKERZ_NROFNODES)
        # run the task
        # 1. start 2 or more containers based on the canary image
        # 2. run function on container 1 and test if it worked on container 2
        
        # tasks.task_done()

def main():
    threading.Thread(target=loop, daemon=True).start()

    http.run(threaded=False)

if __name__ == '__main__':
    main()