import tty


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

    def createContainer(self, nodeName, allNodeIps, networkName):
        print(f"creating container {nodeName}: {self.tagImage}")
        self.client.images.pull(self.tagImage)
        return self.client.containers.run(
            self.tagImage,
            entrypoint="/bin/sh",
            command='-c "echo 1 && /usr/local/bin/champ-node --loglevel=debug --feat-metrics"',
            tty=True,
            name=nodeName,
            environment={
                "CHAMP_INITIAL_PEERS": ",".join(allNodeIps),
                "CHAMP_PRIMARY_WALLET_PASSWORD": "pogpogpogpogpog",
                "CHAMP_GENERATE_PRIMARY_WALLET": "true",
                "CHAMP_GENERATE_JWT_KEYS": "true",
            },
            detach=True,
            network=networkName,
        )

    def createNetwork(self, name):
        print("creating network")
        matches = self.client.networks.list([name])
        if not len(matches):
            self.client.networks.create(name, driver="bridge", check_duplicate=True)

    def createContainers(self, number, networkName):
        allNodeIps = []
        for n in range(0, number):
            name = NODE_NAME_PREFIX + str(n)
            allNodeIps.append(f"/dns4/{name}/tcp/50052")
        for i in range(0, number):
            name = NODE_NAME_PREFIX + str(i)
            self.nodes.append(self.createContainer(name, allNodeIps, networkName))

    def cleanup(self):
        print("cleaning up containers..")
        for node in self.nodes:
            node.stop(timeout=1)
            node.remove()
