import docker

class Task:
  def __init__(self, image, tag, commit):
    self.image = image
    self.tag = tag
    self.commit = commit

  def run(self):
    createContainer(self.image)

def createContainer(image):
  client = docker.from_env()
  network = client.networks.create("pog.network", driver="bridge")
  container1 = client.containers.run(image, name="node1", detach=True)
  container2 = client.containers.run(image, name="node2", detach=True)
  network.connect(container1)
  network.connect(container2)


