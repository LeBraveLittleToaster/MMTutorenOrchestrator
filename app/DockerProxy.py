class PortProxy:

    def __init__(self, offset: int, amount: int):
        self.offset: int = offset
        self.occupiedPorts: [bool] = []
        self.clear_ports(amount)

    def free_port(self, port):
        index: int = port - self.offset
        if 0 < index < len(self.occupiedPorts):
            self.occupiedPorts[index] = True

    def clear_ports(self, amount):
        for i in range(0, amount):
            self.occupiedPorts.append(True)

    def get_free_port(self) -> int or None:
        try:
            index = self.occupiedPorts.index(True)
            self.occupiedPorts[index] = False
            return self.offset + index
        except ValueError:
            print("No free port found")
            return None
