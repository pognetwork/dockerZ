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
        print(f"creating container {nodeName}: {self.tagImage}")
        self.client.images.pull(self.tagImage)
        return self.client.containers.create(
            self.tagImage,
            entrypoint="/bin/sleep",
            command="5000" ,
            name=nodeName,
            ports={'50048/tcp': 50048},
            detach=True,
            network=networkName,
        )

    def createNetwork(self, name):
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
