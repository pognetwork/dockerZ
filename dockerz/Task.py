import docker

class Task:
  def __init__(self, image, tag, commit):
    self.image = image
    self.tag = tag
    self.commit = commit
    self.nodes = []

  def run(self, networkName, NrOfNodes):
    print("running task")
    self.client = docker.from_env()
    self.createContainers(NrOfNodes)
    self.createNetwork(networkName)

  def createContainer(self, nodeName):
    print("creating container")
    return self.client.containers.run(self.image, name=nodeName, detach=True)
    
  def createNetwork(self, name="pog.network"):
    print("creating network")
    network = self.client.networks.create(name, driver="bridge")
    for node in self.nodes:
      network.connect(node)

  def createContainers(self, number):
    for i in range(1, number):
      nodeName = "DockerZ_Node_" + str(i)
      self.nodes.append(self.createContainer(nodeName))
