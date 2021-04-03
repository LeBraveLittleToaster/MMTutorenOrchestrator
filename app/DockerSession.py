import uuid


class DockerSession:
    def __init__(self, container_id, proxy_port):
        self.session_id = uuid.uuid4()
        self.container_id = container_id
        self.proxy_port = proxy_port
