from msilib.schema import Error
import os
from flask import Flask, request

KEY = os.environ.get("DOCKERZKEY")

http = Flask(__name__)
@http.route('/update/<key>', methods=['POST'])
def update(key):
    if key != KEY: return "invalid key", 401

    image = request.args.get("image", default="ghcr.io/pognetwork/champ")
    tag = request.args.get("tag", default="canary")

    print(request.form['foo']) # should display 'bar'
    return 'Received !' # response to your request.