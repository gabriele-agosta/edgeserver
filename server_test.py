import socket
import threading
import sys
import struct

class Server:
    def __init__(self, host, port, mode):
        self.host = host
        self.port = port
        self.mode = mode
        self.socket = self.setSocket()
    
    def setSocket(self):
        if self.mode == "tcp":
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def handle_client(self, conn, addr):
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(5000)
            if not data:
                break
            floats = struct.unpack('f' * (len(data) // 4), data)

            print(f"Received floats: {floats}\n") if len(floats) > 3 else print(f"Received RMS: {floats}\n")

        conn.close()
        print(f"Connection closed by {addr}")

    def TCPServer(self):
        (self.socket).bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

def main():
    mode, port = sys.argv[1], int(sys.argv[2])
    server = Server("127.0.0.1", port, mode)

    if server.mode == "tcp":
        server.TCPServer()

if __name__ == "__main__":
    main()