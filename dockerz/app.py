import os, threading, docker, dockerz.task as task, dockerz.test as test
from flask import Flask, request
from queue import Queue

DOCKERZ_KEY = os.environ.get("DOCKERZ_KEY", "someDefaultKey")
DOCKERZ_NETWORK = os.environ.get("DOCKERZ_NAME", "pog.network")
DOCKERZ_NROFNODES = int(os.environ.get("DOCKERZ_NROFNODES", "2"))

tasks = Queue()
currentTask = None

http = Flask(__name__)


@http.route("/update/<key>", methods=["POST"])
def update(key):
    if key != DOCKERZ_KEY:
        return "invalid key", 401
    print("route reached")

    image = request.form.get("image", default="ghcr.io/pognetwork/champ", type=str)
    tag = request.form.get("tag", default="canary", type=str)
    commit = request.form.get("commit", type=str)

    tasks.put(task.Task(image, tag, commit))
    return str(tasks.qsize())


def worker():
    client = docker.from_env()
    for container in client.containers.list(True):
        if container.name.startswith(task.NODE_NAME_PREFIX):
            print(f"Removing Containers {container.name}...")
            container.stop(timeout=1)

    while True:
        currentTask = tasks.get()
        # 1. start 2 or more containers based on the canary image
        currentTask.run(DOCKERZ_NETWORK, DOCKERZ_NROFNODES, client)
        # 2. run function on container 1 and test if it worked on container 2 (Tests)
        testResults = test.run(currentTask)
        for key, value in testResults.items():
            print(
                f"{key}: {value.passed if 'Pass' else 'Failed - '}{value.passed if '' else value.context}"
            )
            # TestLatestblock: Passed
            # TestSomeTest: Failed - Container could not start
        # 3. Cleanup (stop containers)
        currentTask.cleanup()


def main():
    threading.Thread(target=worker, daemon=True).start()

    http.run(threaded=False)
