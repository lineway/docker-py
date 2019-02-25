import docker

client = docker.DockerClient()

print(client.images.list())



