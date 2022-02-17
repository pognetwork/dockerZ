NODE_NAME_PREFIX = "DockerZ_Node_"
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
    self.createContainers(NrOfNodes)
    self.createNetwork(networkName)

  def createContainer(self, nodeName):
    print(f"creating container {self.tagImage}")
    self.client.images.pull(self.tagImage)
    return self.client.containers.run(self.tagImage, command='', name=nodeName, detach=True, auto_remove=True, remove=True)
    
  def createNetwork(self, name="pog.network"):
    print("creating network")
    network = self.client.networks.create(name, driver="bridge")
    for node in self.nodes:
      network.connect(node)

  def createContainers(self, number):
    for i in range(0, number):
      nodeName = NODE_NAME_PREFIX + str(i)
      self.nodes.append(self.createContainer(nodeName))
