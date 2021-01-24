from server import Server
import selectors


class Select(Server):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.selector = selectors.DefaultSelector()
        self.selector.register(
            fileobj=self.socket,
            events=selectors.EVENT_READ,
            data=self.accept
        )

    @staticmethod
    def do_response(client_socket, request):
        response = "Server response!\n".encode()
        client_socket.send(response)

    def accept(self, server_socket):
        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
        self.selector.register(
            fileobj=client_socket,
            events=selectors.EVENT_READ,
            data=self.send
        )

    def send(self, client_socket):
        request = client_socket.recv(4096)

        if not request:
            self.selector.unregister(client_socket)
            client_socket.close()
            return

        self.do_response(client_socket, request)

    def run(self):
        # event loop
        while True:
            events = self.selector.select()

            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


if __name__ == '__main__':
    server = Select('localhost', 5000)
    server.run()
