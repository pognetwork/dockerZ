import time

NODE_NAME_PREFIX = "DockerZNode"


class Task:
    def __init__(self, image, tag, commit):
        self.image = image
        self.tag = tag
        self.commit = commit
        self.tagImage = f"{self.image}:{self.tag}"
        self.nodes = []

    def run(self, networkName, NrOfNodes, client):
        self.client = client
        print(f"running task. Nr of nodes {NrOfNodes}")
        self.createNetwork(networkName)
        self.createContainers(NrOfNodes, networkName)

    def createContainer(self, nodeName, networkName):
        print(f"creating container {self.tagImage}")
        self.client.images.pull(self.tagImage)
        return self.client.containers.run(
            self.tagImage,
            command="--feat-metrics",
            name=nodeName,
            detach=True,
            auto_remove=True,
            remove=True,
            network=networkName
        )

    def createNetwork(self, name="pog.network"):
        print("creating network")
        matches = self.client.networks.list([name])
        if not len(matches):
            self.client.networks.create(name, driver="bridge", check_duplicate=True)

    def createContainers(self, number, networkName):
        for i in range(0, number):
            nodeName = NODE_NAME_PREFIX + str(i)
            self.nodes.append(self.createContainer(nodeName, networkName))

    def cleanup(self):
        print("cleaning up containers..")
        for node in self.nodes:
            node.stop(timeout=1)
