import dockerz.task as task, requests, time


def run(task: task):
    results = {}
    print("running tests..")
    allTests = [func for func in dir(Tests) if callable(getattr(Tests, func))]
    for tests in allTests:
        results[tests.__name__] = tests()

    print("tests completed.")


def preparingTests(task: task):
    print("preparing tests..")
    for node in task.Task.nodes:
        startTime = int(time.time())
        while response.status_code != 200:
            url = f"http://{node.name}:50048"
            response = requests.get(url)
            if startTime + 60 > int(time.time()):
                return TestResult(False, f"could not start container: {node.name}")
            responses = parseResponse(response.text)
            if responses["grpc_health"] == "1":
                break
    TestResult(True, f"_")


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
    pass

    # http endpoint port 50048
    # get text
    # split new line without #
    # then split by space for hashmap
