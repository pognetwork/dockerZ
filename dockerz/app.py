import os, threading, docker

import dockerz.test as test
import dockerz.webhook as webhook

from .Task import Task, NODE_NAME_PREFIX
from flask import Flask, request
from queue import Queue


DOCKERZ_KEY = os.environ.get("DOCKERZ_KEY", "someDefaultKey")
DOCKERZ_NETWORK = os.environ.get("DOCKERZ_NAME", "pog.network")
DOCKERZ_NROFNODES = int(os.environ.get("DOCKERZ_NROFNODES", "2"))
DOCKERZ_WEBHOOK = os.environ.get("DOCKERZ_WEBHOOK")

tasks = Queue()
currentTask = None

http = Flask(__name__)


@http.route("/update/<key>", methods=["POST"])
def update(key):
    if key != DOCKERZ_KEY:
        return "invalid key", 401
    print("route reached")

    image = request.json["image"]
    tag = request.json["tag"]
    commit = request.json["commit"]

    tasks.put(Task(image, tag, commit))
    return str(tasks.qsize())


def worker():
    client = docker.from_env()
    for container in client.containers.list(True):
        if container.name.startswith(NODE_NAME_PREFIX):
            print(f"Removing Containers {container.name}...")
            container.stop(timeout=1)

    while True:
        currentTask = tasks.get()
        # start 2 or more containers based on the canary image
        currentTask.run(DOCKERZ_NETWORK, DOCKERZ_NROFNODES, client)
        # run function on container 1 and test if it worked on container 2 (Tests)
        testResults = test.run(currentTask, DOCKERZ_NETWORK)
        webhook.run(testResults, DOCKERZ_WEBHOOK, currentTask.commit)
        # Cleanup (stop containers)
        currentTask.cleanup()


def main():

    threading.Thread(target=worker, daemon=True).start()

    http.run(threaded=False, host="0.0.0.0")
