from sys import stdout
import requests

from requests.adapters import HTTPAdapter, Retry
from .Task import Task
import requests, time


def run(task: Task, networkName):
    results = {}
    print("running tests..")
    results["preparingTests"] = PreparingTests(task, networkName)
    for func in dir(Tests):
        test = getattr(Tests, func)
        if callable(test) and not func.startswith("__"):
            results[func] = test(task, networkName)

    print("tests completed.")
    return results


def PreparingTests(task: Task, networkName):
    print("preparing tests..")
    for node in task.nodes:
        response = None
        startTime = int(time.time())
        node.reload()
        ip = node.attrs["NetworkSettings"]["Networks"][networkName]["IPAddress"]
        url = f"http://{ip}:50048"
        time.sleep(5)
        while not response or response.status_code != 200:
            s = requests.Session()
            retries = Retry(
                total=7, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
            )
            s.mount("http://", HTTPAdapter(max_retries=retries))
            response = s.get(url)
            if (startTime + 60) < int(time.time()):
                return TestResult(False, f"could not start container: {node.name}")
            responses = parseResponse(response.text)
            if responses["grpc_health"] == "1":
                break

    return TestResult(True, "")


def parseResponse(text: str):
    lines = text.splitlines()
    lines = filter(lambda a: not a.startswith("#"), lines)
    responses = {}
    for line in lines:
        responses[line.split(" ")[0]] = line.split(" ")[1]
    return responses


class TestResult:
    def __init__(self, passed, context):
        self.passed = passed
        self.context = context


class Tests:
    def TestTests(task):
        return TestResult(True, "Debug Test testing failed")

    def TestPing(task: Task, networkName):
        print(networkName)
        for node in task.nodes:
            node.reload()
            ip = node.attrs["NetworkSettings"]["Networks"][networkName]["IPAddress"]
            url = f"http://{ip}:50048"
            # check if metrics has pings
            s = requests.Session()
            s.mount("http://", HTTPAdapter())
            response = s.get(url)
            responses = parseResponse(response.text)
            peers = responses["connected_peers"]
            total_nodes = task.nodes.len()
            if peers != total_nodes:
                return TestResult(False, f"Only {peers} of {total_nodes} nodes connected.")
        return TestResult(True, "")
