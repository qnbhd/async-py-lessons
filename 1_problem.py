from server import Server


class Problem(Server):

    def __init__(self, host, port):
        super().__init__(host, port)

    @staticmethod
    def send_response(client_socket, request):
        response = "Server response!\n".encode()
        client_socket.send(response)

    def run(self):
        while True:
            client_socket, addr = self.socket.accept()
            print('Connection from', addr)

            while True:
                request = client_socket.recv(4096)

                if not request:
                    break

                self.send_response(client_socket, request)

            client_socket.close()


if __name__ == '__main__':
    server = Problem('localhost', 5000)
    server.run()
