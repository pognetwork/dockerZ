from dockerz.task import Task
import requests, time


def run(task: Task, networkName):
    results = {}
    print("running tests..")
    results["preparingTests"] = preparingTests(task, networkName)
    for func in dir(Tests):
        test = getattr(Tests, func)
        if callable(test) and not func.startswith("__"):
            results[func] = test(task)

    print("tests completed.")
    return results


def preparingTests(task: Task, networkName):
    print("preparing tests..")
    for node in task.nodes:
        response = None
        startTime = int(time.time())
        while not response or response.status_code != 200:
            node.reload()
            ip = node.attrs['NetworkSettings']['Networks'][networkName]['IPAddress']
            url = f"http://{ip}:50048"
            print(url)
            response = requests.get(url, timeout=60)
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
    def testTests(task):
        return TestResult(True, "")

    # http endpoint port 50048
    # get text
    # split new line without #
    # then split by space for hashmap
