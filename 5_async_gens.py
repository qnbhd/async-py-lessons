from server import Server
from select import select
import queue

TO_READ = "read"
TO_WRITE = "write"


class Generators(Server):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.tasks = queue.Queue()
        self.to_read = dict()
        self.to_write = dict()

        self.tasks.put_nowait(self.accept())

    @staticmethod
    def send_response(client_socket, request):
        response = "Server response!\n".encode()
        client_socket.send(response)

    def accept(self):
        while True:
            yield TO_READ, self.socket
            client_socket, addr = self.socket.accept()
            print('Connection from', addr)
            self.tasks.put_nowait(self.send(client_socket))

    def send(self, client_socket):
        while True:
            yield TO_READ, client_socket
            request = client_socket.recv(4096)

            if not request:
                client_socket.close()
                return

            yield TO_WRITE, client_socket
            self.send_response(client_socket, request)

    def run(self):
        # event loop
        while any([self.tasks, self.to_read, self.to_write]):
            while self.tasks.empty():
                ready2read, ready2write, _ = select(
                    self.to_read, self.to_write, []
                )
                for socket in ready2read:
                    task = self.to_read.pop(socket)
                    self.tasks.put_nowait(task)
                for socket in ready2write:
                    task = self.to_write.pop(socket)
                    self.tasks.put_nowait(task)
            try:
                task = self.tasks.get_nowait()
                reason, socket = next(task)
                if reason == TO_READ:
                    self.to_read[socket] = task
                if reason == TO_WRITE:
                    self.to_write[socket] = task
            except StopIteration:
                print('Done')


if __name__ == '__main__':
    server = Generators('localhost', 5000)
    server.run()
