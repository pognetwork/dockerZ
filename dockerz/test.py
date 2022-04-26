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
            results[func] = test(task)

    print("tests completed.")
    return results


def PreparingTests(task: Task, networkName):
    print("preparing tests..")
    ips = []
    for node in task.nodes:
        response = None
        startTime = int(time.time())
        node.reload()
        ip = node.attrs["NetworkSettings"]["Networks"][networkName]["IPAddress"]
        url = f"http://{ip}:50048"
        time.sleep(5)
        while not response or response.status_code != 200:
            print("pog1")
            s = requests.Session()
            retries = Retry(
                total=7, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
            )
            print("pog2")
            s.mount("http://", HTTPAdapter(max_retries=retries))
            response = s.get(url)
            print("pog2.5")
            if (startTime + 60) < int(time.time()):
                print("unpog")
                return TestResult(False, f"could not start container: {node.name}")
            responses = parseResponse(response.text)
            if responses["grpc_health"] == "1":
                break
            print("pog3")

    print("pogchamp")
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

    def TestPing(task):
        # for node in task.nodes:
        # send ping
        # check response
        return TestResult(True, "")
