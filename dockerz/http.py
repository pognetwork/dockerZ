from flask import Flask, request
from app import KEY, tasks
from Task import Task

http = Flask(__name__)
@http.route('/update/<key>', methods=['POST'])
def update(key):
    if key != KEY: return "invalid key", 401

    image = request.form.get("image", default="ghcr.io/pognetwork/champ")
    tag = request.form.get("tag", default="canary")
    commit = request.form.get("commit")

    tasks.append(Task(image, tag, commit))

    return 'Received!'