from server import Server
from select import select


class Select(Server):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.to_monitor = [self.socket]

    @staticmethod
    def send_response(client_socket, request):
        response = "Server response!\n".encode()
        client_socket.send(response)

    def accept(self):
        client_socket, addr = self.socket.accept()
        print('Connection from', addr)
        self.to_monitor.append(client_socket)

    def send(self, client_socket):
        request = client_socket.recv(4096)

        if not request:
            client_socket.close()
            return

        self.send_response(client_socket, request)

    def run(self):
        # event loop
        while True:

            ready2read, _, _ = select(self.to_monitor, [], [])

            for socket in ready2read:
                if socket == self.socket:
                    self.accept()
                else:
                    self.send(socket)


if __name__ == '__main__':
    server = Select('localhost', 5000)
    server.run()
