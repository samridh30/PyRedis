import socket
from pyredis.protocol import encode_message, extract_frame_from_buffer
from pyredis.commands import handle_command

DEFAULT_PORT = 6379
DEFAULT_SERVER = "127.0.0.1"

def handle_client_connection(client_socket):
    buffer = bytearray()
    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            buffer.extend(data)

            frame, frame_size = extract_frame_from_buffer(buffer)

            if frame:
                buffer = buffer[frame_size:]
                result = handle_command(frame)
                client_socket.send(encode_message(result))

    finally:
        client_socket.close()


class Server:
    def __init__(self, port):
        self.port = port
        self._running = False

    def run(self):
        self._running = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._server_socket = server_socket
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((DEFAULT_SERVER, DEFAULT_PORT))
            server_socket.listen()


            while self._running:
                connection, _ = server_socket.accept()
                handle_client_connection(connection)

    def stop(self):
        self._running =  False



