from typing import List

import docker as docker
from docker import DockerClient

from DockerProxy import PortProxy
from DockerSession import DockerSession


class DockerCon:
    def __init__(self, url):
        self.url = url
        self.sessions: List[DockerSession] = []
        self.port_proxy = PortProxy(5678, 4)
        self.client: DockerClient = docker.DockerClient(base_url=url)

    def start_session(self) -> bool:
        port = self.port_proxy.get_free_port()
        if port is None:
            return False
        print("Starting session on proxy port=" + str(port))
        container_id = self.client.containers.run("hashicorp/http-echo",
                                                  command="-listen=:"
                                                          + str(port)
                                                          + " -text=helloworld"
                                                          + str(port),
                                                  ports={port: port},
                                                  detach=True).short_id
        self.sessions.append(DockerSession(container_id, port))
        print("Session started, id=" + container_id)
        return True

    def stop_all_sessions(self):
        for session in self.sessions:
            self.stop_session(session.container_id, session.proxy_port)
        self.sessions = []

    def stop_session(self, container_id, port):
        container = self.client.containers.get(str(container_id))
        if container is not None:
            print("Stopping container " + container_id)
            container.stop()
        else:
            print("Container " + container_id + " already terminated")
        print("Freeing port: " + str(port))
        self.port_proxy.free_port(port)

    def list_container(self):
        return str(self.client.containers.list())

    def list_sessions(self):
        out = "Sessions:\n"
        for session in self.sessions:
            out += " | c_id: " + session.container_id
            out += " | port: " + str(session.proxy_port)
        return out

    def list_ports(self):
        return "offset: " + str(self.port_proxy.offset) + " " + str(self.port_proxy.occupiedPorts)

    def updateList(self) -> [str]:
        stoppedSessions = []
        for session in self.sessions:
            isIn = False
            for container in self.client.containers.list():
                if container.short_id == session.container_id:
                    isIn = True
                    break
            if not isIn:
                stoppedSessions.append(session)
                self.sessions.remove(session)
                self.port_proxy.free_port(session.proxy_port)
        return stoppedSessions
